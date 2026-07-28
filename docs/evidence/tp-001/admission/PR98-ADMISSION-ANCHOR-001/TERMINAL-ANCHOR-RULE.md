# Terminal anchor rule

An append-only admission anchor binds the preceding state-changing event.

This anchor candidate binds PR #98's reviewed head, actual merge commit, ordered parents, merge-tree content relationship, workflow evidence, correction lineage, public/restricted evidence boundary, and non-claims.

The anchor cannot pre-bind its own future merge commit because that commit does not exist until the anchor is merged. Its own repository inclusion, if separately authorized, will be evidenced by the immutable anchor content, Git merge history, resulting tree, and repository CI. A later periodic higher-order lineage anchor may cite it, but an immediate recursive self-anchor is not required.

This rule terminates recursive anchor generation without treating the anchor as self-authorizing.
