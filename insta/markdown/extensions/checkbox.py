from insta.markdown.schemas import (
    register_schema,
    remove_newlines,
    DEFAULT_INDENT_VALUE,
    clean_label,
)

from insta.markdown.build import (
    MarkdownNode
)

from insta.markdown.extensions.base import (
    InSTABaseSchema
)

from insta.utils import (
    NodeMetadata
)

from typing import List


@register_schema(
    "insta_checkbox",
    priority = 0,
    behaves_like = [
        "link"
    ]
)
class InSTACheckboxSchema(InSTABaseSchema):

    attributes = {"role": [
        'checkbox',
    ], "type": [
        'checkbox',
        'radio'
    ]}
    
    def format(
        self, node: MarkdownNode,
        node_metadata: NodeMetadata,
        child_representations: List[str],
        indent_level: int = 0,
        indent_value: str = DEFAULT_INDENT_VALUE,
    ) -> str:
        
        node_metadata = node_metadata or {}

        title = (
            clean_label(node.html_element.attrib.get("name")) or 
            clean_label(node.html_element.attrib.get("title")) or 
            clean_label(node.html_element.attrib.get("aria-label")) or ""
        )

        title_outputs = []

        if len(title) > 0:
            title_outputs.append(title)

        title_outputs.append(
            "checkbox"
        )

        title = " ".join(
            title_outputs
        )

        is_checked = (
            node.html_element.attrib.get("aria-checked") or 
            node.html_element.attrib.get("checked") or 
            node_metadata.get("editable_value")
        )
        
        candidate_id = node_metadata[
            "candidate_id"
        ]

        return '[id: {id}] "{is_checked}" ({title})'.format(
            id = candidate_id,
            is_checked = is_checked,
            title = title
        )
