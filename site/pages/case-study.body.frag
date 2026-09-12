      <section class="page-hero" aria-labelledby="page-title">
        <div class="page-hero-inner">
          <p class="eyebrow">Reference implementation</p>
          <h1 id="page-title">Governed delivery on Azure Container Apps.</h1>
          <p class="page-lead">
            A real engineering pattern for moving a working local application
            into a cloud service while preserving version control, deployment
            traceability, operating safeguards, and an explicit recovery path.
          </p>
          <div class="case-metadata" role="group" aria-label="Case study attributes">
            <span>Real implementation</span>
            <span>Azure</span>
            <span>Cloud operations</span>
            <span>Reference architecture</span>
          </div>
        </div>
      </section>

      <section class="content-section narrow">
        <div class="disclosure">
          <h2>What this case study is</h2>
          <p>
            This is a technical reference implementation, not a client success
            story. MailSweep is a separate product brand. It is not a Tectori
            service line, and no client name, testimonial, or client result is
            implied here.
          </p>
        </div>
      </section>

      <section class="content-section split-section" aria-labelledby="challenge-title">
        <div class="section-heading">
          <p class="eyebrow">The challenge</p>
          <h2 id="challenge-title">Preserve control while the delivery model changes.</h2>
        </div>
        <div class="prose">
          <p>
            MailSweep began as a single-user Windows application for mailbox
            triage. Its cloud variant needed to support Microsoft 365 in a
            hosted operating model while sharing the same core engine and user
            interface with the local product.
          </p>
          <p>
            The engineering question was larger than where to run the code. The
            deployment needed clear version identity, controlled access to
            Azure, separated runtime storage, audit logging, a repeatable test
            path, and a way to detect drift between shared local and cloud
            behavior.
          </p>
        </div>
      </section>

      <section class="soft-band" aria-labelledby="architecture-title">
        <div>
          <div class="section-heading">
            <p class="eyebrow">The implementation</p>
            <h2 id="architecture-title">A shared product core with a controlled cloud edge.</h2>
          </div>
          <div class="practice-grid">
            <article class="practice-item">
              <h3>Shared engine and interface</h3>
              <p>Local and cloud delivery modes share the classification engine and browser interface, with environment-specific behavior kept at the edge.</p>
            </article>
            <article class="practice-item">
              <h3>Azure Container Apps</h3>
              <p>The cloud service runs as a containerized application on Azure, with Azure storage services used for hosted state.</p>
            </article>
            <article class="practice-item">
              <h3>Microsoft 365 scope</h3>
              <p>The hosted service has a deliberate Microsoft and Azure boundary instead of claiming provider support the cloud product does not implement.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="content-section" aria-labelledby="safeguards-title">
        <div class="section-heading">
          <p class="eyebrow">Operating safeguards</p>
          <h2 id="safeguards-title">The delivery record explains what reached production.</h2>
        </div>
        <div class="flow-grid">
          <article class="flow-step">
            <span class="step-number">01</span>
            <h3>Source control</h3>
            <p>Application, deployment, and infrastructure definitions are versioned together in the project repository.</p>
          </article>
          <article class="flow-step">
            <span class="step-number">02</span>
            <h3>Identity</h3>
            <p>The deployment pipeline uses identity federation to authenticate to Azure without storing a long-lived cloud password in the workflow.</p>
          </article>
          <article class="flow-step">
            <span class="step-number">03</span>
            <h3>Version pinning</h3>
            <p>Each production deployment points to a container image tagged with the full source commit identifier.</p>
          </article>
          <article class="flow-step">
            <span class="step-number">04</span>
            <h3>Parity checks</h3>
            <p>Automated checks detect drift in shared administrative logic between the local and cloud delivery modes.</p>
          </article>
          <article class="flow-step">
            <span class="step-number">05</span>
            <h3>Verification</h3>
            <p>Release notes and a running manual test plan document what changed, how to verify it, and which surface is affected.</p>
          </article>
        </div>
      </section>

      <section class="dark-band" aria-labelledby="outcome-title">
        <div class="split-section section">
          <div class="section-heading">
            <p class="eyebrow">Current state</p>
            <h2 id="outcome-title">A live pattern with evidence behind it.</h2>
          </div>
          <div class="prose">
            <p>
              The cloud service runs in production on Azure Container Apps.
              The repository records the product version, source commit,
              container image, deployment definition, shared code boundaries,
              and operator testing expectations.
            </p>
            <p>
              This implementation does not claim a client outcome or a
              fabricated performance result. Its value as evidence is simpler.
              It shows the build standards in working code and operating
              records, not only in a slide deck.
            </p>
          </div>
        </div>
      </section>

      <section class="cta-band">
        <div class="cta-inner">
          <h2>Build cloud operations that can explain themselves.</h2>
          <div class="action-row">
            <a class="button primary" href="/contact">Discuss a cloud project</a>
            <a class="button secondary" href="tel:+16158296802">Call <span class="nowrap">(615) 829-6802</span></a>
          </div>
        </div>
      </section>
