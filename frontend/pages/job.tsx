import React, { useState } from "react";
import { useRouter } from "next/router";
import {
  Box,
  Typography,
  Chip,
  Button,
  Card,
  CardContent,
  Divider,
  IconButton,
  Alert,
} from "@mui/material";
import {
  ArrowBack,
  LocationOn,
  AttachMoney,
  Work,
  AccessTime,
  Bookmark,
  BookmarkBorder,
  Share,
  Business,
  Phone,
  Email,
} from "@mui/icons-material";
import { dummyJobs } from "./jobs";

const Job: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;

  // Find the job by ID
  const job = dummyJobs.find((j) => j.id === id);
  const [isBookmarked, setIsBookmarked] = useState(job?.isBookmarked || false);

  // If job not found
  if (!job) {
    return (
      <Box sx={{ p: 3, textAlign: "center" }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Job not found
        </Alert>
        <Button
          variant="contained"
          startIcon={<ArrowBack />}
          onClick={() => router.push("/jobs")}
        >
          Back to Jobs
        </Button>
      </Box>
    );
  }

  const handleBookmarkToggle = () => {
    setIsBookmarked(!isBookmarked);
  };

  const handleApply = () => {
    // Handle job application logic
    console.log("Applying for job:", job.id);
  };

  const handleShare = () => {
    // Handle sharing logic
    if (navigator.share) {
      navigator.share({
        title: job.title,
        text: `Check out this ${job.title} position at ${job.company}`,
        url: window.location.href,
      });
    } else {
      // Fallback - copy to clipboard
      navigator.clipboard.writeText(window.location.href);
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", backgroundColor: "grey.50" }}>
      {/* Header with back button */}
      <Box
        sx={{
          position: "sticky",
          top: 0,
          backgroundColor: "background.paper",
          zIndex: (theme) => theme.zIndex.appBar,
          px: 2,
          py: 1.5,
          borderBottom: 1,
          borderColor: "divider",
          boxShadow: 1,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <IconButton onClick={() => router.back()}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" sx={{ flex: 1 }}>
            Job Details
          </Typography>
          <IconButton onClick={handleShare}>
            <Share />
          </IconButton>
          <IconButton onClick={handleBookmarkToggle}>
            {isBookmarked ? <Bookmark color="primary" /> : <BookmarkBorder />}
          </IconButton>
        </Box>
      </Box>

      {/* Job Content */}
      <Box sx={{ p: 2 }}>
        {/* Main Job Card */}
        <Card sx={{ mb: 2 }}>
          <CardContent>
            {/* Job Title and Company */}
            <Typography
              variant="h4"
              component="h1"
              sx={{ fontWeight: 600, mb: 1 }}
            >
              {job.title}
            </Typography>
            <Typography
              variant="h6"
              color="text.secondary"
              sx={{ mb: 2, filter: "blur(3px)" }}
            >
              {job.company}
            </Typography>

            {/* Job Details */}
            <Box
              sx={{ display: "flex", flexDirection: "column", gap: 1.5, mb: 3 }}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <LocationOn color="action" />
                <Typography variant="body1">{job.location}</Typography>
              </Box>

              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <AttachMoney sx={{ color: "success.main" }} />
                <Typography
                  variant="body1"
                  sx={{ fontWeight: 600, color: "success.main" }}
                >
                  {job.salary}
                </Typography>
              </Box>

              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <Work color="action" />
                <Typography variant="body1">{job.jobType}</Typography>
              </Box>

              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <AccessTime color="action" />
                <Typography variant="body1">Posted {job.postedTime}</Typography>
              </Box>
            </Box>

            {/* Skills/Tags */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ mb: 1.5, fontWeight: 600 }}>
                Required Skills
              </Typography>
              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                {job.tags.map((tag, index) => (
                  <Chip
                    key={index}
                    label={tag}
                    variant="outlined"
                    color="primary"
                  />
                ))}
              </Box>
            </Box>

            {/* Apply Button */}
            <Box sx={{ display: "flex", gap: 2 }}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                onClick={handleApply}
                sx={{ py: 1.5 }}
              >
                Apply Now
              </Button>
            </Box>
          </CardContent>
        </Card>

        {/* Job Description Card */}
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              Job Description
            </Typography>
            <Typography variant="body1" sx={{ lineHeight: 1.7, mb: 2 }}>
              We are looking for an experienced {job.title.toLowerCase()} to
              join our growing team. This is an excellent opportunity to work on
              diverse projects and develop your skills in a supportive
              environment.
            </Typography>

            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
              Responsibilities:
            </Typography>
            <Typography variant="body1" sx={{ lineHeight: 1.7, mb: 2 }}>
              • Complete installations and repairs to a high standard
              <br />
              • Work safely and follow all health and safety regulations
              <br />
              • Communicate effectively with clients and team members
              <br />
              • Maintain accurate records of work completed
              <br />• Participate in ongoing training and development
            </Typography>

            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
              Requirements:
            </Typography>
            <Typography variant="body1" sx={{ lineHeight: 1.7 }}>
              • Relevant trade qualifications and certifications
              <br />
              • Proven experience in the field
              <br />
              • Strong problem-solving skills
              <br />
              • Excellent attention to detail
              <br />• Full driving license preferred
            </Typography>
          </CardContent>
        </Card>

        {/* Company Info Card */}
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              About {job.company}
            </Typography>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}>
              <Business color="action" />
              <Typography variant="body1">{job.company}</Typography>
            </Box>
            <Typography variant="body1" sx={{ lineHeight: 1.7, mb: 2 }}>
              {job.company} is a leading provider of professional trade services
              with over 10 years of experience. We pride ourselves on quality
              workmanship and excellent customer service.
            </Typography>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" sx={{ mb: 1.5, fontWeight: 600 }}>
              Contact Information
            </Typography>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <Phone color="action" fontSize="small" />
                <Typography style={{ filter: "blur(3px)" }} variant="body2">
                  0161 123 4567
                </Typography>
              </Box>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <Email color="action" fontSize="small" />
                <Typography variant="body2" style={{ filter: "blur(3px)" }}>
                  jobs@{job.company.toLowerCase().replace(/\s+/g, "")}.co.uk
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default Job;
