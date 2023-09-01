from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from typing import Awaitable, Callable

from promplate.llm.base import *
from promplate.prompt import ChatTemplate, Template
from promplate.prompt.template import Context

from .utils import appender, count_position_parameters

PreProcess = Callable[[Context], Context]
PostProcess = PreProcess | Callable[[Context, str], Context]

AsyncPreProcess = Callable[[Context], Awaitable[Context]]
AsyncPostProcess = AsyncPreProcess | Callable[[Context, str], Awaitable[Context]]


class AbstractChain(ABC):
    @abstractmethod
    def run(
        self,
        context: Context,
        complete: Complete | None = None,
    ) -> Context:
        pass

    @abstractmethod
    async def arun(
        self,
        context: Context,
        complete: Complete | AsyncComplete | None = None,
    ) -> Context:
        pass

    complete: Complete | AsyncComplete | None


class Node(AbstractChain):
    def __init__(
        self,
        template: Template | ChatTemplate,
        pre_processes: list[PreProcess | AsyncPreProcess] | None = None,
        post_processes: list[PostProcess | AsyncPostProcess] | None = None,
        complete: Complete | AsyncComplete | None = None,
        **config,
    ):
        self.template = template
        self.pre_processes = pre_processes or []
        self.post_processes = post_processes or []
        self.complete = complete
        self.run_config = config

    @property
    def pre_process(self):
        return appender(self.pre_processes)

    @property
    def post_process(self):
        return appender(self.post_processes)

    @staticmethod
    def _via(
        process: PostProcess | AsyncPostProcess,
        context: Context,
        result: str,
    ) -> Context | Awaitable[Context]:
        if count_position_parameters(process) == 1:
            context = process(context) or context
        else:
            context = process(context, result) or context

    def _apply_pre_processes(self, context: Context):
        for process in self.pre_processes:
            context = process(context) or context
        return context

    def _apply_post_processes(self, context: Context, result: str):
        for process in self.post_processes:
            context = self._via(process, context, result) or context
        return context

    def run(self, context, complete=None):
        complete = complete or self.complete
        assert complete is not None

        context = self._apply_pre_processes(context)
        prompt = self.template.render(context)

        assert isinstance(self.template, ChatTemplate) ^ isinstance(prompt, str)

        result = context["__result__"] = complete(prompt, **self.run_config)

        context = self._apply_post_processes(context, result)

        return context

    async def _apply_async_pre_processes(self, context: Context):
        for process in self.pre_processes:
            if iscoroutinefunction(process):
                context = await process(context) or context
            else:
                context = process(context) or context

        return context

    async def _apply_async_post_processes(self, context: Context, result: str):
        for process in self.post_processes:
            if iscoroutinefunction(process):
                context = await self._via(process, context, result) or context
            else:
                context = self._via(process, context, result) or context

        return context

    async def arun(self, context, complete=None):
        complete = complete or self.complete
        assert complete is not None

        context = await self._apply_async_pre_processes(context)
        prompt = await self.template.arender(context)

        assert isinstance(self.template, ChatTemplate) ^ isinstance(prompt, str)

        if iscoroutinefunction(complete):
            result = context["__result__"] = await complete(prompt, **self.run_config)
        else:
            result = context["__result__"] = complete(prompt, **self.run_config)

        context = await self._apply_async_post_processes(context, result)

        return context

    def next(self, chain: AbstractChain):
        if isinstance(chain, Node):
            return Chain(self, chain)
        else:
            return Chain(self, *chain)

    def __add__(self, chain: AbstractChain):
        return self.next(chain)

    def render(self, context: Context):
        context = self._apply_pre_processes(context)
        return self.template.render(context)

    async def arender(self, context: Context):
        context = await self._apply_async_pre_processes(context)
        return await self.template.arender(context)


class Chain(AbstractChain):
    def __init__(
        self,
        *nodes: AbstractChain,
        complete: Complete | AsyncComplete | None = None,
    ):
        self.nodes = list(nodes)
        self.complete = complete

    def next(self, chain: AbstractChain):
        if isinstance(chain, Node):
            return Chain(*self, chain)
        else:
            return Chain(*self, *chain)

    def __add__(self, chain):
        return self.next(chain)

    def __iter__(self):
        return iter(self.nodes)

    def _run(self, context, complete):
        for node in self.nodes:
            context = node.run(context, node.complete or complete)

        return context

    def run(self, context, complete=None):
        complete = complete or self.complete
        try:
            return self._run(context, complete)
        except JumpTo as jump:
            return jump.chain.run(jump.context or context, complete)

    async def _arun(self, context, complete):
        for node in self.nodes:
            context = await node.arun(context, node.complete or complete)

        return context

    async def arun(self, context, complete=None):
        complete = complete or self.complete
        try:
            return await self._arun(context, complete)
        except JumpTo as jump:
            return await jump.chain.arun(jump.context or context, complete)


class JumpTo(Exception):
    def __init__(self, chain: Node | Chain, context: Context | None = None):
        self.chain = chain
        self.context = context
