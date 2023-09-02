from typing import Type, Union

from piplinetest import BaseTestStep, BasePipLineTest


TestStep = Type[BaseTestStep]

PipLineTest = Type[BasePipLineTest]

Http_Res = Type[Union[dict, str]]
