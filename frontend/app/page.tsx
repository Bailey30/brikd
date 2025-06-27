"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  Badge,
  IconButton,
} from "@mui/material";
import {
  Message,
  Reply,
  LocationOn,
  TrendingUp,
  ArrowForward,
  Notifications,
  Bookmark,
  Work,
} from "@mui/icons-material";
import { DashboardCard } from "@/components/DashboardCard";

export default function Home() {
  const router = useRouter();

  const handleMessagesClick = () => {
    console.log("Navigate to messages");
    // router.push('/messages');
  };

  const handleResponsesClick = () => {
    console.log("Navigate to responses");
    // router.push('/responses');
  };

  const handleLocalJobsClick = () => {
    console.log("Navigate to local jobs");
    router.push("/jobs?location=local");
  };

  const handleHighPaidJobsClick = () => {
    console.log("Navigate to high paid jobs");
    router.push("/jobs?filter=highpaid");
  };

  const handleSavedJobsClick = () => {
    console.log("Navigate to saved jobs");
    // router.push('/saved-jobs');
  };

  const handleApplicationsClick = () => {
    console.log("Navigate to applications");
    // router.push('/applications');
  };

  return (
    <Box sx={{ minHeight: "100vh", backgroundColor: "grey.50" }}>
      {/* Header */}
      <Box
        sx={{
          backgroundColor: "background.paper",
          px: 3,
          py: 3,
          borderBottom: 1,
          borderColor: "divider",
          boxShadow: 1,
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
              Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Welcome back! Here's what's happening with your job search.
            </Typography>
          </Box>
          <IconButton>
            <Badge badgeContent={3} color="error">
              <Notifications />
            </Badge>
          </IconButton>
        </Box>
      </Box>

      {/* Dashboard Cards */}
      <Box sx={{ p: 3 }}>
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, sm: 5 }}>
            <DashboardCard
              title="Messages"
              count={12}
              icon={<Message />}
              color="#2196F3"
              description="New messages from employers"
              onClick={handleMessagesClick}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 5 }}>
            <DashboardCard
              title="Responses"
              count={5}
              icon={<Reply />}
              color="#4CAF50"
              description="Responses to your applications"
              onClick={handleResponsesClick}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6 }}>
            <DashboardCard
              title="Local Jobs"
              count={23}
              icon={<LocationOn />}
              color="#FF9800"
              description="Jobs near Manchester"
              onClick={handleLocalJobsClick}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6 }}>
            <DashboardCard
              title="High Paid Jobs"
              count={8}
              icon={<TrendingUp />}
              color="#9C27B0"
              description="Jobs over £45,000 salary"
              onClick={handleHighPaidJobsClick}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6 }}>
            <DashboardCard
              title="Saved Jobs"
              count={15}
              icon={<Bookmark />}
              color="#E91E63"
              description="Your bookmarked positions"
              onClick={handleSavedJobsClick}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6 }}>
            <DashboardCard
              title="Applications"
              count={28}
              icon={<Work />}
              color="#00BCD4"
              description="Total applications submitted"
              onClick={handleApplicationsClick}
            />
          </Grid>
        </Grid>

        {/* Recent Activity Section */}
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
            Recent Activity
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 2,
                      mb: 2,
                    }}
                  >
                    <Avatar sx={{ backgroundColor: "success.main" }}>
                      <Reply />
                    </Avatar>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        Application Response
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        PowerTech Solutions responded to your Electrician
                        application
                      </Typography>
                    </Box>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ ml: "auto" }}
                    >
                      2 hours ago
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 2,
                      mb: 2,
                    }}
                  >
                    <Avatar sx={{ backgroundColor: "primary.main" }}>
                      <Message />
                    </Avatar>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        New Message
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        AquaFix Services sent you a message about the Plumber
                        position
                      </Typography>
                    </Box>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ ml: "auto" }}
                    >
                      5 hours ago
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 2,
                      mb: 2,
                    }}
                  >
                    <Avatar sx={{ backgroundColor: "warning.main" }}>
                      <LocationOn />
                    </Avatar>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        New Local Job
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        3 new Carpenter jobs posted in Manchester area
                      </Typography>
                    </Box>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ ml: "auto" }}
                    >
                      1 day ago
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Box>
  );
}
