    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "{{SITE_URL}}/#organization",
        "name": "Tectori",
        "url": "{{SITE_URL}}/",
        "logo": "{{SITE_URL}}/assets/{{LOGO_FILENAME}}",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "{{ADDRESS_STREET}}",
          "addressLocality": "{{ADDRESS_LOCALITY}}",
          "addressRegion": "{{ADDRESS_REGION}}",
          "postalCode": "{{ADDRESS_POSTAL_CODE}}",
          "addressCountry": "US"
        },
        "sameAs": [
          "{{LINKEDIN_URL}}",
          "{{GITHUB_URL}}"
        ],
        "description": "Founder-led cloud, cybersecurity, compliance, IT operations, fractional leadership, and AI governance consulting for regulated and growing organizations.",
        "founder": {
          "@type": "Person",
          "name": "Jonathan Bowker",
          "jobTitle": "Founder and Principal Consultant",
          "url": "{{SITE_URL}}/about",
          "@id": "{{SITE_URL}}/#jonathan-bowker",
          "sameAs": "{{GITHUB_URL}}",
          "hasCredential": [
            {
              "@type": "EducationalOccupationalCredential",
              "name": "Certified Information Systems Security Professional (CISSP)"
            },
            {
              "@type": "EducationalOccupationalCredential",
              "name": "SABSA Chartered Security Architect, Foundation Certificate (SCF)"
            },
            {
              "@type": "EducationalOccupationalCredential",
              "name": "Payment Card Industry Professional (PCIP)"
            },
            {
              "@type": "EducationalOccupationalCredential",
              "name": "Payment Card Industry Internal Security Assessor (ISA)"
            },
            {
              "@type": "EducationalOccupationalCredential",
              "name": "SANS SEC545, GenAI and LLM Application Security, 2026"
            }
          ],
          "award": "Finalist, Top 3, Nashville Security Leader of the Year, 2022",
          "alumniOf": [
            {
              "@type": "EducationalOrganization",
              "name": "Georgia Institute of Technology"
            },
            {
              "@type": "EducationalOrganization",
              "name": "Kennesaw State University"
            }
          ]
        },
        "areaServed": {
          "@type": "Country",
          "name": "United States"
        },
        "contactPoint": {
          "@type": "ContactPoint",
          "contactType": "business inquiries",
          "telephone": "{{PHONE_SCHEMA}}",
          "url": "{{SITE_URL}}/contact"
        },
        "knowsAbout": [
          "Cloud architecture and operations",
          "Cybersecurity",
          "Compliance and risk management",
          "IT operations",
          "Fractional CIO and CISO leadership",
          "AI governance",
          "ISO/IEC 42001",
          "NIST AI Risk Management Framework"
        ]
      }
    </script>
