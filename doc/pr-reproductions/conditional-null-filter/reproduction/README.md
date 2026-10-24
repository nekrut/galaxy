# Screenshot reproduction

These are browser screenshots of a local harness using Galaxy's real `Node.vue`, `SVGConnection.vue`, terminal validation and Pinia stores. They are not screenshots of a deployed patched Galaxy Main. The banner reads the actual invalid-connection store. No warnings or edge colors are manually assigned.

`steps.json` retains the merge and two null-filter schemas/connections from the authenticated ATAC candidate editor export. The two upstream grouping operations are represented by typed `list:list` collection inputs. `provenance.json` records the source and this reduction. The original step identifiers are retained, hence the displayed step numbers are not consecutive.

To reproduce at Galaxy commit `63c851669b25f21f3cc3f0a2d6bf5255f8fd128d`:

1. Install the client's pinned dependencies with `pnpm install --frozen-lockfile`.
2. Copy `App.vue`, `main.ts` and `steps.json` into `client/src/connection-repro/`.
3. Copy `datatypes.json` from this directory into that directory.
4. Copy the HTML and Vite configuration here into `client/`.
5. In `client`, run `pnpm exec vite --config connection-repro.config.mjs`.
6. Run the adjacent `capture_reproduction.py Before` using Python with Playwright and Chrome. It asserts two invalid edges and no browser errors.
7. Apply the PR's `terminals.ts` change, then run `capture_reproduction.py After`. It asserts zero invalid edges and no browser errors.

The UI harness is retained on this separate public assets branch. The Galaxy PR contains the terminal fix and regression tests; it does not install this harness or any screenshot assets into Galaxy.
