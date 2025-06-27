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
  Description,
} from "@mui/icons-material";
import { useRouter } from "next/router";

interface JobAdProps {
  icon: any;
  title: string;
  description: string;
  onClick?: () => void;
}

const AccountCard: React.FC<JobAdProps> = ({
  icon,
  title,
  description,
  onClick,
}) => {
  const theme = useTheme();
  const router = useRouter();

  return (
    <Card
      sx={{
        height: "clamp(20%, 20vh, 175px)",
        // minHeight: "150px",
        // maxHeight: "200px",
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
      onClick={onClick}
    >
      <CardContent
        sx={{
          height: "100px",
          display: "flex",
          //   flexDirection: "column",
          //   justifyContent: "space-between",
          p: 2,
          //   "&:last-child": { pb: 2 },
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
          {icon}
        </Box>

        {/* Job details */}
        <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 1 }}>
          <Typography variant="body2" fontWeight="500" noWrap>
            {title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ fontWeight: 400 }}
            noWrap
          >
            {description}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default AccountCard;
