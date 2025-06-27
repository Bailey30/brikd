"use client";

import JobAdCard from "@/components/JobAdCard";
import React, { useState } from "react";
import { Box, Typography, List, ListItem } from "@mui/material";
import { useRouter } from "next/router";
interface JobData {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  jobType: string;
  postedTime: string;
  tags: string[];
  isBookmarked: boolean;
}

export const dummyJobs: JobData[] = [
  {
    id: "1",
    title: "Qualified Electrician",
    company: "PowerTech Solutions",
    location: "Manchester, UK",
    salary: "£35,000 - £45,000",
    jobType: "Full-time",
    postedTime: "2 days ago",
    tags: ["18th Edition", "City & Guilds", "Commercial", "Domestic"],
    isBookmarked: false,
  },
  {
    id: "2",
    title: "Experienced Plumber",
    company: "AquaFix Services",
    location: "London, UK",
    salary: "£38,000 - £50,000",
    jobType: "Full-time",
    postedTime: "1 day ago",
    tags: [
      "Gas Safe",
      "Boiler Installation",
      "Bathroom Fitting",
      "Emergency Repairs",
    ],
    isBookmarked: true,
  },
  {
    id: "3",
    title: "Carpenter - Kitchen Specialist",
    company: "CraftWood Ltd",
    location: "Birmingham, UK",
    salary: "£32,000 - £42,000",
    jobType: "Full-time",
    postedTime: "3 days ago",
    tags: ["Kitchen Fitting", "Joinery", "MDF", "Hardwood", "Power Tools"],
    isBookmarked: false,
  },
  {
    id: "4",
    title: "Bricklayer",
    company: "Stonework Professionals",
    location: "Leeds, UK",
    salary: "£30,000 - £40,000",
    jobType: "Full-time",
    postedTime: "4 hours ago",
    tags: ["Block Work", "Pointing", "Extensions", "New Builds"],
    isBookmarked: false,
  },
  {
    id: "5",
    title: "HVAC Technician",
    company: "Climate Control Systems",
    location: "Edinburgh, UK",
    salary: "£40,000 - £55,000",
    jobType: "Full-time",
    postedTime: "1 week ago",
    tags: ["Air Conditioning", "Heating Systems", "F-Gas", "Commercial"],
    isBookmarked: true,
  },
  {
    id: "6",
    title: "Roofer",
    company: "Peak Roofing Services",
    location: "Bristol, UK",
    salary: "£33,000 - £43,000",
    jobType: "Full-time",
    postedTime: "5 days ago",
    tags: ["Slate", "Tiles", "Flat Roofing", "Guttering", "Safety Harness"],
    isBookmarked: false,
  },
  {
    id: "7",
    title: "Apprentice Electrician",
    company: "Northern Electric",
    location: "Manchester, UK",
    salary: "£18,000 - £22,000",
    jobType: "Apprenticeship",
    postedTime: "2 days ago",
    tags: ["Level 3", "NVQ", "Training Provided", "Domestic Wiring"],
    isBookmarked: false,
  },
  {
    id: "8",
    title: "Plasterer",
    company: "Smooth Finish Ltd",
    location: "Liverpool, UK",
    salary: "£28,000 - £38,000",
    jobType: "Contract",
    postedTime: "6 days ago",
    tags: ["Skimming", "Rendering", "Dry Lining", "Artex Removal"],
    isBookmarked: true,
  },
  {
    id: "9",
    title: "Tiler",
    company: "Premium Tiling Co",
    location: "Glasgow, UK",
    salary: "£30,000 - £40,000",
    jobType: "Full-time",
    postedTime: "3 days ago",
    tags: ["Ceramic", "Porcelain", "Natural Stone", "Bathroom", "Kitchen"],
    isBookmarked: false,
  },
  {
    id: "10",
    title: "Multi-Trade Maintenance",
    company: "Property Solutions Group",
    location: "Cardiff, UK",
    salary: "£32,000 - £38,000",
    jobType: "Full-time",
    postedTime: "1 day ago",
    tags: [
      "Basic Plumbing",
      "Basic Electrical",
      "Carpentry",
      "Painting",
      "Social Housing",
    ],
    isBookmarked: false,
  },
];

// Usage example with the JobAdCard component:
/*
import { dummyJobs } from './dummyJobsData';
import JobAdCard from './JobAdCard';

const JobsList = () => {
  const [jobs, setJobs] = useState(dummyJobs);

  const handleBookmarkToggle = (jobId: string) => {
    setJobs(prevJobs =>
      prevJobs.map(job =>
        job.id === jobId
          ? { ...job, isBookmarked: !job.isBookmarked }
          : job
      )
    );
  };

  const handleJobClick = (jobId: string) => {
    console.log(`Clicked job with ID: ${jobId}`);
    // Navigate to job details page
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '16px' }}>
      {jobs.map(job => (
        <JobAdCard
          key={job.id}
          title={job.title}
          company={job.company}
          location={job.location}
          salary={job.salary}
          jobType={job.jobType}
          postedTime={job.postedTime}
          tags={job.tags}
          isBookmarked={job.isBookmarked}
          onBookmarkToggle={() => handleBookmarkToggle(job.id)}
          onClick={() => handleJobClick(job.id)}
        />
      ))}
    </div>
  );
};
*/
const JobSearchPage = () => {
  return (
    <Box sx={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Sticky Header */}
      <Box
        sx={{
          position: "sticky",
          top: 0,
          backgroundColor: "background.paper",
          zIndex: (theme) => theme.zIndex.appBar,
          px: 3,
          py: 2,
          borderBottom: 1,
          borderColor: "divider",
          boxShadow: 1,
        }}
      >
        <Typography variant="h4" component="h1" sx={{ m: 0, fontWeight: 600 }}>
          Jobs
        </Typography>
      </Box>

      {/* Scrollable Jobs List */}
      <Box
        sx={{
          flex: 1,
          overflow: "auto",
          px: 3,
          py: 2,
        }}
      >
        <List sx={{ p: 0 }}>
          {dummyJobs.map((job) => (
            <ListItem key={job.id} sx={{ px: 0, pb: 2.5 }}>
              <JobAdCard {...job} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
};

export default JobSearchPage;
