from ..containers import MultipleContainers, Optimizers
from ..hooks import ClassifierHook, FinetunerHook
from .base_adapter import BaseGCAdapter
from .utils import default_optimizer_tuple, with_opt


class Classifier(BaseGCAdapter):
    """
    Wraps [ClassifierHook][pytorch_adapt.hooks.classification.ClassifierHook].
    """

    hook_cls = ClassifierHook

    def init_hook(self, hook_kwargs):
        opts = with_opt(list(self.optimizers.keys()))
        self.hook = self.hook_cls(opts=opts, **hook_kwargs)


class Finetuner(Classifier):
    """
    Wraps [FinetunerHook][pytorch_adapt.hooks.classification.FinetunerHook].
    """

    hook_cls = FinetunerHook

    def get_default_containers(self):
        optimizers = Optimizers(default_optimizer_tuple(), keys=["C"])
        return MultipleContainers(optimizers=optimizers)

    def get_key_enforcer(self):
        ke = super().get_key_enforcer()
        ke.requirements["optimizers"].remove("G")
        return ke
