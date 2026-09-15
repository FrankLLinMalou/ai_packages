# External extensions and runtime requirements

The package embeds pinned, maximally redistributable working-tree snapshots of
all three upstream projects. Do not install a duplicate upstream skill for a
capability already present under `modules/`.

Bundled files and active runtime capability are different. External action may
still be needed for:

- registering a Ponytail plugin, hook, command set, or MCP server with the host;
- installing Python, R, npm, browser, font, document, or system dependencies;
- authenticating to literature databases, issue trackers, publishers, APIs, or
  other services;
- obtaining lawful institutional or paid access;
- moving to a newer upstream revision than the pinned snapshot;
- publishing, deploying, sending, or writing to an external system.

## Authorization and cost rules

1. State which exact capability is unavailable from the embedded instructions
   and files alone.
2. Inspect the selected embedded script, manifest, hook, or adapter before
   proposing execution or installation. Do not execute repository scripts
   blindly.
3. Put dependencies, permissions, persistence, network access, expected cost,
   and outputs in the plan. Starting the orchestrator does not authorize them.
4. Prefer an already available host capability over registering duplicate
   plugins or installing redundant dependencies.
5. For an upstream update, compare licenses and behavior, pin the new commit,
   regenerate manifests, run all validations, and obtain approval for material
   workflow changes.
6. Stop after one clear installation or registration failure. Report the
   blocker instead of retrying indefinitely.
