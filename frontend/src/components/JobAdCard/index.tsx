import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  useTheme,
} from "@mui/material";
import {
  LocationOn,
  AttachMoney,
  Work,
  AccessTime,
  Bookmark,
  BookmarkBorder,
} from "@mui/icons-material";
import { useRouter } from "next/router";

interface JobAdProps {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  jobType: string;
  postedTime: string;
  tags?: string[];
  isBookmarked?: boolean;
  onBookmarkToggle?: () => void;
  onClick?: () => void;
}

const JobAdCard: React.FC<JobAdProps> = ({
  id,
  title,
  company,
  location,
  salary,
  jobType,
  postedTime,
  tags = [],
  isBookmarked = false,
  onBookmarkToggle,
  onClick,
}) => {
  const theme = useTheme();
  const router = useRouter();

  const handleJobClick = (jobId: string) => {
    router.push(`/job?id=${jobId}`);
    //   onClick()
  };
  return (
    <Card
      sx={{
        height: "25vh",
        minHeight: "200px",
        maxHeight: "280px",
        width: "100%",
        borderRadius: 2,
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        cursor: onClick ? "pointer" : "default",
        transition: "transform 0.2s ease, box-shadow 0.2s ease",
        "&:hover": onClick
          ? {
              transform: "translateY(-2px)",
              boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            }
          : {},
        position: "relative",
        overflow: "hidden",
      }}
      onClick={() => handleJobClick(id)}
    >
      <CardContent
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          p: 2,
          "&:last-child": { pb: 2 },
        }}
      >
        {/* Header with title and bookmark */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            mb: 1,
          }}
        >
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography
              variant="h6"
              component="h3"
              sx={{
                fontWeight: 600,
                fontSize: "1.1rem",
                lineHeight: 1.2,
                mb: 0.5,
                overflow: "hidden",
                textOverflow: "ellipsis",
                display: "-webkit-box",
                WebkitLineClamp: 2,
                WebkitBoxOrient: "vertical",
              }}
            >
              {title}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ fontWeight: 500, filter: "blur(3px)" }}
            >
              {company}
            </Typography>
          </Box>

          {onBookmarkToggle && (
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                onBookmarkToggle();
              }}
              sx={{ ml: 1, flexShrink: 0 }}
            >
              {isBookmarked ? <Bookmark color="primary" /> : <BookmarkBorder />}
            </IconButton>
          )}
        </Box>

        {/* Job details */}
        <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 1 }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
            <LocationOn sx={{ fontSize: "1rem", color: "text.secondary" }} />
            <Typography variant="body2" color="text.secondary" noWrap>
              {location}
            </Typography>
          </Box>

          <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
            <AttachMoney sx={{ fontSize: "1rem", color: "success.main" }} />
            <Typography
              variant="body2"
              sx={{ fontWeight: 600, color: "success.main" }}
              noWrap
            >
              {salary}
            </Typography>
          </Box>

          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
              <Work sx={{ fontSize: "1rem", color: "text.secondary" }} />
              <Typography variant="body2" color="text.secondary">
                {jobType}
              </Typography>
            </Box>
            <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
              <AccessTime sx={{ fontSize: "1rem", color: "text.secondary" }} />
              <Typography variant="body2" color="text.secondary">
                {postedTime}
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Tags */}
        {tags.length > 0 && (
          <Box
            sx={{
              display: "flex",
              flexWrap: "wrap",
              gap: 0.5,
              mt: 1,
              overflow: "hidden",
              maxHeight: "40px",
            }}
          >
            {tags.slice(0, 3).map((tag, index) => (
              <Chip
                key={index}
                label={tag}
                size="small"
                variant="outlined"
                sx={{
                  height: "20px",
                  fontSize: "0.75rem",
                  borderRadius: "10px",
                }}
              />
            ))}
            {tags.length > 3 && (
              <Chip
                label={`+${tags.length - 3}`}
                size="small"
                variant="outlined"
                sx={{
                  height: "20px",
                  fontSize: "0.75rem",
                  borderRadius: "10px",
                  color: "text.secondary",
                }}
              />
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default JobAdCard;
