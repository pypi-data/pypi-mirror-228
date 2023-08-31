from django import forms
from django.utils.functional import cached_property
from wagtail.admin.staticfiles import versioned_static
from wagtail.blocks.struct_block import (
    StructBlock as LegacyStructBlock,
    StructBlockAdapter as LegacyStructBlockAdapter,
)
from wagtail.telepath import register


class SBStructBlock(LegacyStructBlock):
    class Meta:
        form_classname = "sb-structblock"
        settings_fields = []


class StructBlockAdapter(LegacyStructBlockAdapter):
    js_constructor = "wagtail_sb_structblock.blocks.structblock"

    def js_args(self, block):
        name, value, meta = super().js_args(block)

        if block.meta.settings_fields:
            meta["settingsFields"] = block.meta.settings_fields

        return [
            name,
            value,
            meta,
        ]

    @cached_property
    def media(self):
        return forms.Media(
            js=[
                versioned_static("wagtail_sb_structblock/js/structblock.js"),
            ],
            css={
                "all": [
                    versioned_static("wagtail_sb_structblock/css/structblock.css"),
                ],
            },
        )


register(StructBlockAdapter(), SBStructBlock)
