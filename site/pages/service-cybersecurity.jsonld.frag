    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "Service",
            "@id": "{{SITE_URL}}/service-cybersecurity#service",
            "name": "Cybersecurity",
            "url": "{{SITE_URL}}/service-cybersecurity",
            "description": "Security control design and ownership, hardening baselines, and identity and access management across Active Directory, Azure, and Microsoft 365.",
            "serviceType": "Cybersecurity",
            "provider": {
              "@id": "{{SITE_URL}}/#organization"
            },
            "areaServed": {
              "@type": "Country",
              "name": "United States"
            }
          },
          {
            "@type": "BreadcrumbList",
            "@id": "{{SITE_URL}}/service-cybersecurity#breadcrumb",
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
              },
              {
                "@type": "ListItem",
                "position": 3,
                "name": "Cybersecurity",
                "item": "{{SITE_URL}}/service-cybersecurity"
              }
            ]
          }
        ]
      }
    </script>
