"use client";

import React from "react";

const ProfilePage = () => {
  const user = {
    name: "Jane Doe",
    email: "jane@example.com",
    role: "Software Engineer",
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Profile</h1>
      <p>
        <strong>Name:</strong> {user.name}
      </p>
      <p>
        <strong>Email:</strong> {user.email}
      </p>
      <p>
        <strong>Role:</strong> {user.role}
      </p>
    </div>
  );
};

export default ProfilePage;
