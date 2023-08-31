# Hoppr JQ Filter

A Hoppr plugin to filter components out of the delivered sbom using jq syntax.

It works as the intersect of "includes" and "excludes".

- Any components not found with the includes will be removed
- Any components found with the excludes will be removed

```yml
  SampleStage:
    plugins:
    - name: "hoppr_jq_filter.plugin"
      config:
        delete_excluded: True
        purl_regex_includes: []
        purl_regex_excludes: []
        jq_expression_includes: []
        jq_expression_excludes: []
```

- `delete_excluded`
  - A flag indicating if the plugin should delete any excluded components found in `collect_root_dir`
- `purl_regex_includes`
  - A list of regular expressions for purls that should remain in the SBOM
- `purl_regex_excludes`
  - A list of regular expressions to remove purls that match in the SBOM
- `jq_expression_includes`
  - A list of jq expressions for components that should remain in the SBOM
- `jq_expression_excludes`
  - A list of jq expressions to remove components that match in the SBOM

## Examples

### Only keep generic components in the SBOM

```yml
  SampleStage:
    plugins:
    - name: "hoppr_jq_filter.plugin"
      config:
        purl_regex_includes:
          - "^pkg:generic"
```

### Remove any purl with `controlled` in the name

```yml
  SampleStage:
    plugins:
    - name: "hoppr_jq_filter.plugin"
      config:
        purl_regex_excludes:
          - "controlled"
```

## Debugging

If you are having trouble filtering out components, you can easily debug using `jq` directly.

1. Run hoppr bundle with a `-v` and review the logs.
1. This plugin will print all of the jq queries used and the matching purls found.
1. You can `cat your-sbom.cdx.json | jq '<your query>'` to debug.
