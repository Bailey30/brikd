"use client";

import AccountCard from "@/components/AccountCard";
import { Button } from "@mui/material";
import { Box, List, ListItem, Typography } from "@mui/material";
import React from "react";
import AccountBoxOutlinedIcon from "@mui/icons-material/AccountBoxOutlined";
import DisplaySettingsOutlinedIcon from "@mui/icons-material/DisplaySettingsOutlined";
import ManageAccountsOutlinedIcon from "@mui/icons-material/ManageAccountsOutlined";

const SearchPreferencesPage = () => {
  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        p: "1rem",
      }}
    >
      <Typography variant="h4" component="h1" sx={{ m: 0, fontWeight: 600 }}>
        Profile
      </Typography>
      <Box>
        <List>
          <ListItem sx={{ px: 0, pb: 2.5 }}>
            <AccountCard
              icon={<AccountBoxOutlinedIcon />}
              title="Profile"
              description="Complete your profile."
            />
          </ListItem>
          <ListItem sx={{ px: 0, pb: 2.5 }}>
            <AccountCard
              icon={<DisplaySettingsOutlinedIcon />}
              title="Profile"
              description="Complete your profile."
            />
          </ListItem>
          <ListItem sx={{ px: 0, pb: 2.5 }}>
            <AccountCard
              icon={<ManageAccountsOutlinedIcon />}
              title="Profile"
              description="Complete your profile."
            />
          </ListItem>
        </List>
        <List sx={{ width: "80%", m: "auto" }}>
          <ListItem>
            <Button fullWidth variant="outlined" color="error">
              Log Out
            </Button>
          </ListItem>
          <ListItem>
            <Button fullWidth variant="outlined" color="error">
              Delete Account
            </Button>
          </ListItem>
        </List>
      </Box>
    </Box>
  );
};

export default SearchPreferencesPage;
