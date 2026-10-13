# Set add-on product configuration

<!-- diataxis: how-to -->

This guide shows you how to provide Zope `<product-config>` sections that
add-ons read for their own configuration.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Step 1: define the configuration

Set `product_config` in your `instance.yaml` to a dictionary of dictionaries.
Each top-level key becomes a section name, and its dictionary provides that
section's key/value pairs:

```yaml
default_context:
    product_config:
        my_addon:
            setting1: value1
            setting2: value2
```

## Step 2: check the generated output

This renders a `<product-config>` section in `zope.conf`:

```text
<product-config my_addon>
    setting1 value1
    setting2 value2
</product-config>
```

The add-on reads these values through the Zope configuration API.

## Next steps

- {doc}`/reference/basic-config` -- Reference for `product_config` and the
  other core settings.
