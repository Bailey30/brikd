"use client";

import React, { useState } from "react";

const JobSearchPage = () => {
  const [query, setQuery] = useState("");

  const jobs = [
    {
      id: 1,
      title: "Frontend Developer",
      company: "Tech Co.",
      location: "London",
    },
    {
      id: 2,
      title: "Backend Engineer",
      company: "API Inc.",
      location: "Remote",
    },
    {
      id: 3,
      title: "DevOps Engineer",
      company: "Cloudify",
      location: "Bristol",
    },
  ];

  const filtered = jobs.filter((job) =>
    job.title.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Job Search</h1>
      <input
        type="text"
        placeholder="Search job titles..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ padding: "0.5rem", width: "100%", marginBottom: "1rem" }}
      />
      <ul>
        {filtered.map((job) => (
          <li key={job.id} style={{ marginBottom: "1rem" }}>
            <strong>{job.title}</strong>
            <br />
            {job.company} — {job.location}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobSearchPage;
