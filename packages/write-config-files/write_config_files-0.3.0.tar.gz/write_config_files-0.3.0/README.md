# write config files

This tool allows you to render templated config files and write them out.

This can be used to manage personal config files with different settings in
different places (e.g. work/personal) or without committing secrets to a git
repo.

## getting started

You will need a file to configure the templates and a file to provide context
variables. By default these are names `templates.yaml` and `context.yaml`,
respectively. e.g:

### templates

The root template directory is relative to the templates file. Each entry in the
`template_groups` must be a group of templates that will be written to the
output directory. All template files must be listed explicitly.

Templates may be written to a different name than the name of the template file
by setting the `destination` attribute. The written files may be made executable
by making `is_executable` true.

e.g:

```yaml
root_template_dir: ./templates
template_groups:
-   output_dir: '~'
    templates:
    -   template: .editorconfig
    -   template: .zshrc
-   output_dir: ~/.config/
    templates:
    -   template: git/config
    -   template: git/ignore
-   output_dir: ~/.local/bin
    templates:
    -   template: my_script.py
        destination: my-script
        is_executable: true
```

### context

This will be parsed from YAML into a plain dictionary and used as the template
context. A context file be provided. If no context is needed, make it an empty
dict:

```yaml
{}
```

## usage

### `write`

Render the templates and write the output files.

```console
usage: write-config-files write [-h] [-t TEMPLATES] [-c CONTEXT] [-f] [-d]

options:
  -h, --help            show this help message and exit
  -t TEMPLATES, --templates TEMPLATES
                        path to config file (default: templates.yaml)
  -c CONTEXT, --context CONTEXT
                        path to context file (default: context.yaml)
  -f, --force           overwrite existing files
  -d, --dry-run         render templates but do not write files
```

### `diff`

Show the diff between the current files and what would be written with `write`.

```console
usage: write-config-files diff [-h] [-t TEMPLATES] [-c CONTEXT] [-p PAGER]

options:
  -h, --help            show this help message and exit
  -t TEMPLATES, --templates TEMPLATES
                        path to config file (default: templates.yaml)
  -c CONTEXT, --context CONTEXT
                        path to context file (default: context.yaml)
  -p PAGER, --pager PAGER
                        the pager to use to display each diff (default: no pager)
```
