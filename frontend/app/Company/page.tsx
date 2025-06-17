"use client";

import React from "react";

const CompanyPage = () => {
  const company = {
    name: "Tech Innovations Ltd.",
    location: "Manchester, UK",
    description: "Building the future with cutting-edge tech solutions.",
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Company Info</h1>
      <p>
        <strong>Name:</strong> {company.name}
      </p>
      <p>
        <strong>Location:</strong> {company.location}
      </p>
      <p>
        <strong>Description:</strong> {company.description}
      </p>
    </div>
  );
};

export default CompanyPage;
