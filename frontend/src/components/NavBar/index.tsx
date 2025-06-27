"use client";

import React from "react";
import { useRouter } from "next/navigation";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";

import HomeIcon from "@mui/icons-material/Home";
import WorkIcon from "@mui/icons-material/Work";
import BusinessIcon from "@mui/icons-material/Business";
import PersonIcon from "@mui/icons-material/Person";

const navItems = [
  { label: "Home", icon: <HomeIcon />, href: "/" },
  { label: "Jobs", icon: <WorkIcon />, href: "/jobs" },
  { label: "Company", icon: <BusinessIcon />, href: "/company" },
  { label: "Profile", icon: <PersonIcon />, href: "/profile" },
];

const NavBar = () => {
  const router = useRouter();
  const theme = useTheme();
  // Match screens md and up (desktop)
  const isDesktop = useMediaQuery(theme.breakpoints.up("md"));

  // Track selected nav item by current pathname
  const [value, setValue] = React.useState(0);

  React.useEffect(() => {
    const index = navItems.findIndex(
      (item) => item.href === window.location.pathname
    );
    setValue(index === -1 ? 0 : index);
  }, [typeof window !== "undefined" ? window.location.pathname : null]);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
    router.push(navItems[newValue].href);
  };

  return (
    <BottomNavigation
      value={value}
      onChange={handleChange}
      showLabels={isDesktop} // show labels only on desktop
      sx={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        borderTop: "1px solid",
        borderColor: "divider",
        zIndex: (theme) => theme.zIndex.appBar,
        maxWidth: 480,
        margin: "0 auto",
      }}
    >
      {navItems.map(({ label, icon }) => (
        <BottomNavigationAction
          key={label}
          label={label}
          icon={icon}
          sx={{
            minWidth: 0,
            // On mobile, shrink icon and hide label (labels controlled by showLabels prop)
            ".MuiBottomNavigationAction-label": {
              fontSize: "0.75rem",
            },
          }}
        />
      ))}
    </BottomNavigation>
  );
};

export default NavBar;
