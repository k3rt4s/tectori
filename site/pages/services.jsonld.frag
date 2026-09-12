    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "CollectionPage",
            "@id": "{{SITE_URL}}/services#webpage",
            "name": "Services | Tectori",
            "url": "{{SITE_URL}}/services",
            "description": "Tectori's six consulting service lines, from fractional CIO and CISO leadership to cloud, cybersecurity, compliance, IT operations, and agentic AI.",
            "publisher": {
              "@id": "{{SITE_URL}}/#organization"
            },
            "mainEntity": {
              "@type": "ItemList",
              "itemListElement": [
                {
                  "@type": "ListItem",
                  "position": 1,
                  "name": "Fractional CIO and CISO leadership",
                  "url": "{{SITE_URL}}/service-fractional-leadership"
                },
                {
                  "@type": "ListItem",
                  "position": 2,
                  "name": "Cloud architecture and operations",
                  "url": "{{SITE_URL}}/service-cloud-architecture"
                },
                {
                  "@type": "ListItem",
                  "position": 3,
                  "name": "Cybersecurity",
                  "url": "{{SITE_URL}}/service-cybersecurity"
                },
                {
                  "@type": "ListItem",
                  "position": 4,
                  "name": "Compliance and risk management",
                  "url": "{{SITE_URL}}/service-compliance-risk"
                },
                {
                  "@type": "ListItem",
                  "position": 5,
                  "name": "IT operations",
                  "url": "{{SITE_URL}}/service-it-operations"
                },
                {
                  "@type": "ListItem",
                  "position": 6,
                  "name": "Agentic AI orchestration",
                  "url": "{{SITE_URL}}/service-agentic-ai"
                }
              ]
            }
          },
          {
            "@type": "BreadcrumbList",
            "@id": "{{SITE_URL}}/services#breadcrumb",
            "itemListElement": [
              {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "{{SITE_URL}}/"
              },
              {
                "@type": "ListItem",
                "position": 2,
                "name": "Services",
                "item": "{{SITE_URL}}/services"
              }
            ]
          }
        ]
      }
    </script>
