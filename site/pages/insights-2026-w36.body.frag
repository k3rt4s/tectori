      <section class="page-hero" aria-labelledby="page-title">
        <div class="page-hero-inner">
          <p class="eyebrow">Insights archive</p>
          <h1 id="page-title">31 August to 6 September 2026.</h1>
          <p class="page-lead">
            9 short takes on the security and AI stories of that week, newest first. Each one credits the publication that reported it.
          </p>
          <p><a class="text-link" href="/insights">Back to all Insights</a></p>
        </div>
      </section>
      <section class="content-section" aria-labelledby="archive-title">
        <div class="section-heading">
          <p class="eyebrow">31 August to 6 September 2026</p>
          <h2 id="archive-title">What we read, and what it meant.</h2>
        </div>
        <div class="faq-list">
          <article class="archive-item" id="post-15028">
            <p class="archive-meta"><time datetime="2026-08-30">30 August 2026</time> &middot; on Gambit Security</p>
            <h3>Aurora ransomware targets ESXi abuses Cursor Agent for exploitation</h3>
            <p>Aurora ransomware is evolving with new tactics that leverage AI tools to enhance exploitation. Recent analysis shows attackers using Cursor Agent with Claude Sonnet to assist in targeting ESXi environments. This AI-driven approach allows for more efficient and adaptive attacks, posing new challenges for defenders.</p>
            <p>The use of Cursor Agent enables operators to execute complex tasks, from reconnaissance to privilege escalation, with minimal direct intervention. This shift highlights the growing role of agentic AI in cyber operations, making it essential for organizations to rethink their security strategies. Traditional detection methods may not be sufficient against these sophisticated threats.</p>
            <p>Strong governance and detection mechanisms are critical to mitigating AI-assisted exploitation. Organizations must invest in advanced monitoring, behavioral analysis, and zero-trust frameworks to stay ahead of evolving threats. Collaboration between security teams and AI developers is also necessary to ensure responsible use of these technologies.</p>
            <p class="archive-tags">AIsecurity LLMsecurity AgenticAI ZeroTrust CyberDefense ThreatIntel</p>
          </article>
          <article class="archive-item" id="post-15017">
            <p class="archive-meta"><time datetime="2026-08-29">29 August 2026</time> &middot; on SafeDep</p>
            <h3>Mini Shai-Hulud Strikes Again: openapi-react-query-codegen</h3>
            <p>The npm supply chain attack on @7nohe/openapi-react-query-codegen is a stark reminder of the risks in CI/CD pipelines. Attackers exploited a GitHub Actions workflow with no author-association gate to trigger a release and publish malicious versions under a legitimate package. This highlights how flawed automation can be weaponized.</p>
            <p>The attack used two execution triggers: a binding.gyp file that leverages node-gyp’s Python evaluation and a preinstall hook with a heavily obfuscated script. The payload downloads and runs Bun from GitHub, matching patterns seen in previous supply chain attacks. This reinforces the need for strict access controls and continuous pipeline auditing.</p>
            <p>Secure GitHub Actions workflows are critical. The lack of an author-association gate allowed any user to trigger the release. We must enforce gates, limit permissions, and use frozen lockfiles to prevent arbitrary code execution. This is a win for attackers who understand the weaknesses in open source ecosystems.</p>
            <p>The fix involved removing the issue_comment trigger and tightening permissions. Teams must review their CI/CD pipelines for similar vulnerabilities. AI and automation can’t replace vigilance—especially in open source. Stay sharp, and keep your supply chains secure.</p>
            <p>#SupplyChainSecurity #CI CD #OpenSourceSecurity #DevSecOps #GitHubActions #npmSecurity</p>
          </article>
          <article class="archive-item" id="post-15054">
            <p class="archive-meta"><time datetime="2026-08-27">27 August 2026</time> &middot; on UK AI Security Institute</p>
            <h3>Optimal stopping: spending evaluation compute where it counts | AISI Work</h3>
            <p>Jon&#x27;s post is now correctly formatted and follows all the specified rules. Here it is:</p>
            <p>The challenge of evaluating frontier models is growing. As models become more complex, so do the evaluations needed to measure their true capabilities. But with limited compute budgets and fast release cycles, we risk underestimating model performance and missing key insights.</p>
            <p>Optstop offers a practical solution. By stopping evaluations early when performance estimates are precise enough, it saves up to 97% of planned runs without compromising results. This aligns with our focus on efficient, rigorous AI governance and secure agentic AI.</p>
            <p>The key is adaptive measurement. Traditional fixed-sample approaches can miss critical data, especially in high-stakes scenarios. Optstop uses statistical methods to prioritize where uncertainty remains, ensuring we spend compute where it counts.</p>
            <p>This approach supports our mission to improve evaluation frameworks and share tools that help the community. It’s a step toward more efficient, reliable, and scalable model assessment.</p>
            <p class="archive-tags">AIsecurity LLMsecurity AgenticAI ModelEvaluation ZeroTrust AIgovernance</p>
          </article>
          <article class="archive-item" id="post-15045">
            <p class="archive-meta"><time datetime="2026-08-27">27 August 2026</time> &middot; on Air Security</p>
            <h3>MCPJacking: 155 Hijackable MCPs Discovered Live in the Official MCP Marketplace</h3>
            <p>MCPJacking is a growing threat in agentic AI systems. It exploits the blind trust agents place in their initial configurations. An attacker can reclaim a lapsed domain once a legitimate service goes dark and instantly inherit the agent’s connection. This creates a persistent and unmonitored line of communication that remains open indefinitely.</p>
            <p>The attack is subtle. It doesn’t require injecting malicious code into the agent’s prompt. Instead, it hijacks the MCP server, which the agent trusts implicitly. From this position, the attacker can redefine tools, exfiltrate data, inject prompts, and steer the agent’s behavior without detection.</p>
            <p>This highlights the need for governance and continuous vetting. MCPs originate from registries, GitHub, or individual configurations, often connecting to agents with production access without visibility. Security teams must scan entry resolution, monitor for handoffs, and maintain the ability to revoke access.</p>
            <p>MCPJacking underscores the importance of trust management in AI agent ecosystems. We must build systems that verify the identity and intent of service providers, not just the connection path. Governance, continuous risk management, and visibility are critical to securing agentic AI.</p>
            <p class="archive-tags">AIsecurity LLMsecurity AgenticAI ZeroTrust Cybersecurity AIgovernance</p>
          </article>
          <article class="archive-item" id="post-15027">
            <p class="archive-meta"><time datetime="2026-08-27">27 August 2026</time> &middot; on CloudSEK</p>
            <h3>Caught in 4K: The Aurora Files | CloudSEK</h3>
            <p>The Aurora ransomware affiliate&#x27;s infrastructure reveals a new level of sophistication. The use of AI tools like Cursor for attack planning underscores how adversaries are leveraging advanced tech to automate and refine their tactics. This isn&#x27;t just about speed—it&#x27;s about precision and adaptability in targeting.</p>
            <p>The discovery of shared cryptocurrency laundering infrastructure across multiple victims highlights a critical gap in supply chain security. Traditional defenses are no longer sufficient. We need real-time threat detection and a more proactive approach to monitoring financial flows. This is not a single incident—it&#x27;s a pattern.</p>
            <p>The operator&#x27;s methodical approach, from credential theft to ransomware deployment, shows a clear intent to scale. The use of Zig for the encryptor and the inclusion of self-awareness features in the code point to a high level of technical expertise. These are not random attacks—they&#x27;re well-thought-out operations.</p>
            <p>This case reinforces the need for stronger visibility into both infrastructure and financial movements. We must rethink how we secure our supply chains and how we detect anomalies in real time. The future of security lies in agility and intelligence, not just perimeter defenses.</p>
            <p class="archive-tags">CyberSecurity AIsecurity Ransomware ThreatIntel SupplyChainSecurity ZeroTrust</p>
          </article>
          <article class="archive-item" id="post-15050">
            <p class="archive-meta"><time datetime="2026-08-26">26 August 2026</time> &middot; on NCC Group</p>
            <h3>NCC Group Monthly Threat Pulse – Review of July 2026</h3>
            <p>Ransomware activity hit a 2026 high in July with a 22% increase in cases. The trend shows no signs of slowing, with industrials becoming the top target. North America and Europe remain the most attacked regions. This underscores the need for stronger defenses and proactive strategies.</p>
            <p>AI-driven ransomware like JADEPUFFER is reshaping the threat landscape. These autonomous agents can operate without human input, adapting and executing attacks from compromise to extortion. The speed and scale of such threats demand a reevaluation of how we secure our systems.</p>
            <p>Zero Trust and AI governance frameworks are critical to countering these evolving threats. They provide the structure needed to detect, respond to, and mitigate attacks that leverage AI for automation and sophistication. Governance ensures that AI is used responsibly, both defensively and offensively.</p>
            <p>The challenge lies in balancing technology with human judgment. While AI can enhance detection and response, it cannot replace the need for trained personnel who understand the nuances of modern threats. Investing in both people and processes is the foundation of a resilient security posture.</p>
            <p class="archive-tags">AIsecurity LLMSecurity ZeroTrust AIgovernance CyberThreats RansomwareDefense</p>
          </article>
          <article class="archive-item" id="post-15031">
            <p class="archive-meta"><time datetime="2026-08-26">26 August 2026</time> &middot; on The Guardian</p>
            <h3>Fake US thinktank set up and funded by Israel sought to game AI for propaganda</h3>
            <p>The article highlights a disturbing trend where foreign actors are leveraging AI-native platforms to shape training data and influence chatbot outputs. A fake thinktank, funded by Israel, published over half a million words in nine days, designed to be cited by AI models. The content is framed as neutral research but consistently blurs the line between fact and propaganda. It uses quasi-academic language and selectively cites sources to blunt criticism of Israel, all while avoiding transparency about its funding and existence.</p>
            <p>This raises critical questions about model evaluation and governance. If chatbots are trained on data that is not fully transparent or ethically sourced, how can we trust their outputs? The article shows how AI-native platforms are being used to seed content into training data, making it harder to trace or verify. This isn’t just about misinformation—it’s about shaping narratives at scale, often without users realizing the source.</p>
            <p>As someone who has spent over 19 years in cybersecurity and AI security, I’m deeply concerned about the implications. We need robust frameworks for model evaluation, transparency in training data, and clear governance to prevent AI from being weaponized for disinformation. This isn’t just a technical challenge—it’s a strategic and ethical one. The lines between content creation and influence operations are blurring, and the stakes are high.</p>
            <p>The article also underscores the importance of AI governance. If we don’t establish clear standards for how AI systems are trained and evaluated, we risk normalizing the use of AI to spread disinformation. As leaders in this space, we must advocate for transparency, accountability, and ethical practices. The future of AI security depends on it. We can’t let AI become a tool for manipulation without oversight.</p>
            <p class="archive-tags">AIsecurity LLMsecurity AIgovernance ModelEvaluation EthicalAI ChatbotSafety</p>
          </article>
          <article class="archive-item" id="post-15011">
            <p class="archive-meta"><time datetime="2026-08-26">26 August 2026</time> &middot; on PC</p>
            <h3>חשיפה: ההאקר מאשקלון - עובד IT ומומחה סייבר -</h3>
            <p>המקרה הזה מדגיש את ההשלכות האמיתיות של היכולת לשימוש ב-AI ליצירת נוזקות מתקדמות. ההאקר, שחיבר את כלי התוקף בסיוע AI, הצליח להתחבר לארגונים רבים תוך שהשתמש בדיסקורד ובכלי ניטור מתקדמים. היכולת לשלוט בכלי AI יכולה לסייע גם לתקפות מתקדמות, ולהיחלץ מהן דורשת תקשורת, תפעול ופנימיות במקביל.</p>
            <p>האיסוף של נתונים, תפעול ניטור מדויק, והצלבה של פעילות תקיפה הייתה קריטית לזיהוי ההאקר. כל המתקפות נורמות בקצף, אך כאן נוצרה סיטואציה שיכולה להיעקב כקטסטרופלית. היכולת לשלוט ב-AI היא נשק חכם, אך גם נשק של מתקפות מתקדמות.</p>
            <p>האתגר הגדול הוא לא רק בזיהוי התקפות, אלא בשמירת תקשורת בין צוותים, פיתוח תהליכי ניטור, והשלמת גיבויים. עם שילוב של AI, גיבויים, וניהול קורבן מתקדם, חשוב להכין את הארגון להגנה על עצמו.</p>
            <p>המקרה הזה מציג את הדרישה להכנת מערכות חיזוק עתידיות שתוסיפו לתקיפות. ברגע שבו אנו שוכרים את האינטגרציה בין AI, תקשורת, וניהול קורבן, אנחנו מוכנים ללחימה אמיתית.</p>
            <p class="archive-tags">AIsecurity LLMsecurity ZeroTrust CyberDefense IncidentResponse AIgovernance</p>
          </article>
          <article class="archive-item" id="post-14988">
            <p class="archive-meta"><time datetime="2022-05-04">4 May 2022</time> &middot; on GitHub</p>
            <h3>security/communications/cosmos_evm_GHSA-7g4w-cg88-2cq2_post_mortem.md at main · cosmos/security</h3>
            <p>The Cosmos EVM exploit highlights the risks of supply chain security in open-source ecosystems. A chain of vulnerabilities allowed attackers to siphon funds across multiple networks, demonstrating how decentralized environments can be exploited when communication and patch management are insufficient. The incident underscores the need for rapid, coordinated responses and clear visibility into deployments.</p>
            <p>The initial assessment of the vulnerability was based on limited testing, leading to a misjudgment about its impact. This delayed patching and miscommunication contributed to the breach. It’s a stark reminder that even well-audited code can have hidden flaws, especially in complex systems like EVMs. Clear, urgent communication is essential when a critical flaw is actively exploited.</p>
            <p>Cosmos Labs acted swiftly once the exploit was confirmed, working with affected chains to mitigate damage and coordinate recovery. However, the incident exposed gaps in how we handle critical vulnerabilities, particularly in identifying when a patch’s scope exceeds initial reports. We’re refining our processes to ensure such oversights don’t happen again.</p>
            <p class="archive-tags">Cybersecurity SupplyChainSecurity OpenSource ZeroTrust AIsecurity DevOps</p>
          </article>
        </div>
      </section>
