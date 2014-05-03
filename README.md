weechat-xfer-scp
================

A [Weechat](http://www.weechat.org) plugin for moving files obtained through DCC to an offsite location using SCP. Optionally you can remove the files after they've been successfully sent.



Commands
========

Use `/xfer_scp` to see available commands


Configuration
=============

Type `/set plugins.var.python.xfer_scp.*` to see configuration settings.

NOTE: The variable `plugins.var.python.xfer_scp.patternlist` is managed by the commands, and only used as a persisted storage. Avoid setting this variable on your own and use the provided commands.

Usage
=======

1. Configure your SCP settings
2. Define patterns and corresponding directories using `/xfer_scp add <regexp> <remote_dir>`
3. Recieve a file and it will be sent via SCP if it matches a defined regular expression


Roadmap
=========

    * Allow files to be deleted after being sent
    * Find a better way to persist pattern sets
    * Default operation for non-matching files
    * Command completion
