import React from "react";
import { useRouter } from "next/router";
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
} from "@mui/icons-material";

interface DashboardCardProps {
  title: string;
  count: number;
  icon: React.ReactNode;
  color: string;
  description: string;
  onClick: () => void;
}

export const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  count,
  icon,
  color,
  description,
  onClick,
}) => {
  return (
    <Card
      sx={{
        height: "160px",
        cursor: "pointer",
        transition: "all 0.3s ease",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: 4,
        },
        background: `linear-gradient(135deg, ${color}15 0%, ${color}25 100%)`,
        border: `1px solid ${color}30`,
      }}
      onClick={onClick}
    >
      <CardContent
        sx={{ height: "100%", display: "flex", flexDirection: "column", p: 3 }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            mb: 2,
          }}
        >
          <Avatar
            sx={{
              backgroundColor: color,
              width: 48,
              height: 48,
            }}
          >
            {icon}
          </Avatar>
          <IconButton size="small" sx={{ color: "text.secondary" }}>
            <ArrowForward />
          </IconButton>
        </Box>

        <Box sx={{ flex: 1 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 700, color: color, mb: 0.5 }}
          >
            {count}
          </Typography>
          <Typography
            variant="h6"
            sx={{ fontWeight: 600, mb: 0.5, color: "text.primary" }}
          >
            {title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ fontSize: "0.85rem" }}
          >
            {description}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

const DashboardHomepage: React.FC = () => {
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
          <Grid item xs={12} sm={6}>
            <DashboardCard
              title="Messages"
              count={12}
              icon={<Message />}
              color="#2196F3"
              description="New messages from employers"
              onClick={handleMessagesClick}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <DashboardCard
              title="Responses"
              count={5}
              icon={<Reply />}
              color="#4CAF50"
              description="Responses to your applications"
              onClick={handleResponsesClick}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <DashboardCard
              title="Local Jobs"
              count={23}
              icon={<LocationOn />}
              color="#FF9800"
              description="Jobs near Manchester"
              onClick={handleLocalJobsClick}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <DashboardCard
              title="High Paid Jobs"
              count={8}
              icon={<TrendingUp />}
              color="#9C27B0"
              description="Jobs over £45,000 salary"
              onClick={handleHighPaidJobsClick}
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
};

export default DashboardHomepage;
