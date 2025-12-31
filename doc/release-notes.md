# Release notes

## Upcoming release


### New Features and Major Changes

* [Include comparison and plotting features PR #1](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/1)
* [Include generation of geojson for network validation PR #3](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/3)
* [Finalize workflow, visualization, add CI and documentation PR #6](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/6)
* [Add documentation with MkDocs style PR #20](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/20)

### Minor Changes and bug-fixing

* [Add PR template PR #25](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/25)
* [Improve README.md PR #27](https://github.com/pypsa-meets-earth/pypsa-earth-status/pull/27)


## Release Process

* Checkout a new release branch ``git checkout -b release-v0.x.x``.

* Finalise release notes at ``doc/release_notes.md``.

* Update version number in ``config.yaml``.

* Open, review and merge pull request for branch ``release-v0.x.x``.
  Make sure to close issues and PRs or the release milestone with it (e.g. closes #X).
  Run ``pre-commit run --all`` locally and fix any issues.

* Update and checkout your local `main` and tag a release with ``git tag v0.x.x``, ``git push``, ``git push --tags``. Include release notes in the tag message using Github UI.

* Send announcement on the `PyPSA-Earth Discord channel <https://discord.gg/AnuJBk23FU>`_.
