"""
The `hoppr-jq-filter` filter uses jq syntax to remove components from the SBOM.
"""
# pylint: disable=no-name-in-module

import json

from pathlib import Path
from shutil import rmtree
from typing import Any, List

from hoppr import BomAccess, Component, HopprContext, HopprPlugin, Result, hoppr_process
from hoppr.constants import BomProps
from hoppr_cyclonedx_models.cyclonedx_1_4 import Scope
from jq import compile as jq_compile

from hoppr_jq_filter import __version__


def _jq_query(expression: str, query: Any) -> List[str]:
    return [component["purl"] for component in jq_compile(expression).input(query).all()]


class JQFilterPlugin(HopprPlugin):
    """
    Class for Hoppr plugin for the `hoppr-jq-filter` plugin.
    """

    bom_access = BomAccess.FULL_ACCESS
    products: List[str] = []

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        """
        Constructor with Hoppr framework arguments (context and config)
        """
        self.combined_jq_expression_includes: list[str] = []
        self.combined_jq_expression_excludes: list[str] = []

        if isinstance(config, dict):
            purl_regex_includes: List[str] = config.get("purl_regex_includes", [])
            purl_regex_excludes: List[str] = config.get("purl_regex_excludes", [])
            self.combined_jq_expression_includes = config.get("jq_expression_includes", [])
            self.combined_jq_expression_excludes = config.get("jq_expression_excludes", [])

            self.combined_jq_expression_includes += [
                f'.components[] | select(.purl != null) | select(.purl|test("{regex}"))'
                for regex in purl_regex_includes
            ]
            self.combined_jq_expression_excludes += [
                f'.components[] | select(.purl != null) | select(.purl|test("{regex}"))'
                for regex in purl_regex_excludes
            ]

        super().__init__(context, config)

    def get_version(self) -> str:
        """
        __version__ required for all HopprPlugin implementations
        """
        return __version__

    def delete_collected_component(self, comp: Component):
        """
        Method that iterates through component properties and deletes any directory properties in the
        collect root directory.
        """
        for prop in comp.properties:
            if BomProps.COLLECTION_DIRECTORY == prop.name and prop.value:
                dir_path = Path(self.context.collect_root_dir / prop.value)
                self.get_logger().info(f"deleting - {dir_path}")
                try:
                    rmtree(dir_path)
                except OSError as exception:
                    self.get_logger().error(
                        f'unable to delete {dir_path} associated with excluded component {comp.purl}'
                    )
                    self.get_logger().error(str(exception))

    @hoppr_process
    def pre_stage_process(self) -> Result:
        """
        Convert the bom into a jsonable dictionary, filter with JQ, and then update the `scope` field.
        """
        sbom_jsonable_dict = json.loads(self.context.delivered_sbom.json())

        self.get_logger().debug("## jq include expressions")
        purl_keep: list[str] = []
        for expression in self.combined_jq_expression_includes:
            self.get_logger().debug(f"- expression '{expression}'", indent_level=1)
            purls = _jq_query(expression, sbom_jsonable_dict)
            self.get_logger().debug(f"purls - {purls}", indent_level=1)
            purl_keep += purls

        self.get_logger().debug("## jq exclude expressions")
        purl_remove: list[str] = []
        for expression in self.combined_jq_expression_excludes:
            self.get_logger().debug(f"- expression '{expression}'", indent_level=1)
            purls = _jq_query(expression, sbom_jsonable_dict)
            self.get_logger().debug(f"purls - {purls}", indent_level=1)
            purl_remove += purls

        if self.combined_jq_expression_includes and self.context.delivered_sbom.components:
            for component in self.context.delivered_sbom.components:
                if component.purl in purl_keep:
                    component.scope = Scope.required

        if self.combined_jq_expression_excludes and self.context.delivered_sbom.components:
            for component in self.context.delivered_sbom.components:
                if component.purl in purl_remove:
                    component.scope = Scope.excluded

        self.get_logger().flush()

        return Result.success(return_obj=self.context.delivered_sbom)

    @hoppr_process
    def post_stage_process(self) -> Result:
        """
        Convert the bom into a jsonable dictionary, filter with JQ, and then update the `scope` field.
        """
        delete_excluded = True
        if self.config is not None:
            delete_excluded = self.config.get("delete_excluded", True)

        if delete_excluded:
            for comp in self.context.delivered_sbom.components:
                self.get_logger().debug("## jq include expressions")
                if str(comp.scope) in {'excluded', 'Scope.excluded'}:
                    self.delete_collected_component(comp)

        self.get_logger().flush()

        return Result.success(return_obj=self.context.delivered_sbom)
