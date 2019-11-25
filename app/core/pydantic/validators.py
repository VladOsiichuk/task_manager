from app.core.exceptions import DBError


async def validate_on_unique(model, field, value):
    field_attr = getattr(model, field, None)
    if field_attr is not None:
        instance = await model.query.where(field_attr == value).gino.first()
        if instance:
            raise DBError("This field is not unique")


async def primary_key_exists(model, field, value):
    field_attr = getattr(model, field, None)
    if field_attr is not None:
        if not await model.query.where(field_attr == value).gino.exists():
            raise DBError("Not found")
    return value
