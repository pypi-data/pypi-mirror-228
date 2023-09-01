===========================
collective.tiles.discussion
===========================

Tile for showing most recent discussion items.


Features
--------

- "Latest comments" tile with several fields to determine which discussion items to show.

Inspiration was taken from ``collective.portlet.discussion``.


Installation
------------

Install collective.tiles.discussion by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.tiles.discussion


and then running ``bin/buildout``.

You probably want to add a tile management package as well, for example ``plone.app.mosaic``.


Usage
-----

* Create a Classic UI Plone Site.
* In the Discussion control panel globally enable comments.
* In the Content Settings control panel enable comments on Page, or any content type that you want.
* Add one or more comments.
* Go to the Add-ons control panel.
* Activate ``plone.app.mosaic`` or some other tile management package.
* Activate ``collective.tiles.discussion``.
* Create a page.
* Set its display to ``layout_view`` for Mosaic.
* Edit the page.  The layout view should be active now.
* Insert a "Latest comments" tile, configure it, and save the page.
* Now the tile should show a list with the latests comments.

Note that there is also a "Discussions" tile in ``plone.app.standardtiles``.
This shows the comments of the current page, plus an add-form for a new comment.


Filter on review states
-----------------------

In the tile you can filter on review state if you want.
By default Discussion Items have only one state: published.  In this case a filter is not needed.

In the Discussion control panel you can enable comment moderation.
This enables a workflow with more states.
Comments start in the pending state, and can be published, rejected, or marked as spam.

Currently, in Plone 6.0.6, without filter, an anonymous user will see Discussion Items from the states published, rejected, and spam.
So you may want to explicitly filter on the published state in the tile, and possibly pending.


Contribute
----------

If you are having issues, or want to contribute a bugfix or feature, please let us know.

- Issue Tracker: https://github.com/collective/collective.tiles.discussion/issues
- Source Code: https://github.com/collective/collective.tiles.discussion


License
-------

The project is licensed under the GPLv2.
