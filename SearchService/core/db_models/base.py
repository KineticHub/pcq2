from model_utils.models import TimeStampedModel, UUIDModel


class AbstractBaseModel(UUIDModel, TimeStampedModel):
    """Represents our base model with common shared fields."""

    class Meta:
        abstract = True
        ordering = ("-created",)
