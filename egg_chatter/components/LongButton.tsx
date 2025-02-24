import React from "react";

interface LongButtonProps {
  text: string;
  status?: "active" | "inactive"
  children?: React.ReactNode; 
}

const LongButton = ({ text, status = "inactive", children }: LongButtonProps) => {

    const statusColors = {
        active: "bg-customYellow", 
        inactive: "bg-customGray", 
    };

    const dynamicBgColor = statusColors[status]

    return (
        <div className={`${dynamicBgColor} p-4 rounded-md`}>
        <p>{text}</p>
        {children}
        </div>
    );
};

export default LongButton;
