    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "Service",
            "@id": "{{SITE_URL}}/service-it-operations#service",
            "name": "IT operations",
            "url": "{{SITE_URL}}/service-it-operations",
            "description": "Repeatable and documented administration for Windows, Active Directory, Azure, IIS, and Microsoft 365, with dry runs, plan records, and rollback reporting.",
            "serviceType": "IT operations",
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
            "@id": "{{SITE_URL}}/service-it-operations#breadcrumb",
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
                "name": "IT operations",
                "item": "{{SITE_URL}}/service-it-operations"
              }
            ]
          }
        ]
      }
    </script>
