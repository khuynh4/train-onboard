import React from 'react';
import { ProSidebar, Menu, MenuItem, SidebarHeader, SidebarFooter, SidebarContent} from 'react-pro-sidebar';
import { Link } from 'react-router-dom';
import { IoMdToday } from 'react-icons/io';
import { BsCalendar } from 'react-icons/bs';
import { CgProfile } from 'react-icons/cg';
import { RiTeamLine } from 'react-icons/ri';
import { CgTemplate } from 'react-icons/cg';
import { Col } from 'react-bootstrap';
import 'react-pro-sidebar/dist/css/styles.css';

export function TraineeSidebar (props)  {
    const { name, onBrandChange } = props;
    return (
        <div className="sidebar">
            <ProSidebar>
                <SidebarHeader>
                    <br />
                    <Col><h5 className="title">{ name }</h5></Col>
                    <br />
                </SidebarHeader>
                <SidebarContent>
                    <Menu>
                        <MenuItem icon={ <IoMdToday /> }>
                            <Link to="/user/dashboard">Dashboard</Link>
                        </MenuItem>
                        <MenuItem icon={ <BsCalendar /> }>
                            <Link to="/user/calendar">Calendar</Link>
                        </MenuItem>
                        <MenuItem icon={ <CgProfile/> }>
                            <Link to="/user/user-profile">My Profile</Link>
                        </MenuItem>
                        <MenuItem icon={ <RiTeamLine />}>
                            <Link to="#">My Team</Link>
                        </MenuItem>
                        <MenuItem icon={ <CgTemplate /> }>
                            <Link to="#">My Trainings</Link>
                        </MenuItem>
                    </Menu>
                </SidebarContent>
                <SidebarFooter>
                    <br />
                    <div>
                        <Link to="#" style={{color: "gray", marginRight: 10, marginLeft: 10}}>Home</Link>
                        |
                        <Link to="#" style={{color: "gray", marginRight: 10, marginLeft: 10}}>About</Link>
                        |
                        <Link to="#" style={{color: "gray", marginLeft: 10, marginRight: 10}}>Contact</Link>
                    </div>
                    <br />
                </SidebarFooter>
            </ProSidebar>
        </div>
    )
    
}