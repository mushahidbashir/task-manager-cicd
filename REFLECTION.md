# Reflection

Each stage of this pipeline protects against a different kind of mistake. The lint stage
(black + flake8) catches style and formatting inconsistencies before they ever reach a
reviewer — I saw this firsthand when my first CI run failed at the Lint step because my
files were missing trailing newlines and flake8 was using stricter default settings than
my local Black config. The test stage protects against actual logic errors: when I
intentionally broke a test by changing an expected response value, the pipeline caught it
immediately and failed the build, exactly as it should have. The deploy stage protects
production from ever receiving code that hasn't been verified — it doesn't check anything
itself, it just refuses to run unless everything before it succeeded.

The order matters because each stage is a gate for the one after it. If deploy ran before
test, a broken commit (like my intentionally failing test) could have been "deployed" to
production despite never passing validation, defeating the entire purpose of having tests
in the first place. The `needs: test` condition is what enforces this order — without it,
GitHub Actions would run both jobs in parallel, and deploy could finish before test even
reported a result.

One thing I'd add to make this closer to a real production setup is a test matrix running
against multiple Python versions (3.10, 3.11, 3.12), since real users won't all be on the
same interpreter version I tested locally. I'd also replace the simulated deploy step with
an actual deployment to a free-tier host like Render, using a deploy hook stored as a
GitHub Secret rather than just an echo statement.