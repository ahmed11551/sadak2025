import React from 'react';
import styled from 'styled-components';
import { 
  BarChart3, 
  Users, 
  Building2, 
  Target, 
  FileText, 
  Settings,
  LogOut
} from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';

const SidebarContainer = styled.aside<{ isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e9ecef;
  z-index: 1000;
  transform: ${props => props.isOpen ? 'translateX(0)' : 'translateX(-100%)'};
  transition: transform 0.3s ease;
  
  @media (min-width: 769px) {
    transform: translateX(0);
  }
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
`;

const Logo = styled.div`
  font-size: 20px;
  font-weight: 700;
  color: #007bff;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SidebarNav = styled.nav`
  padding: 20px 0;
`;

const NavList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const NavItem = styled.li`
  margin-bottom: 4px;
`;

const NavLink = styled.button<{ active: boolean }>`
  width: 100%;
  padding: 12px 20px;
  border: none;
  background: ${props => props.active ? '#e3f2fd' : 'transparent'};
  color: ${props => props.active ? '#007bff' : '#6c757d'};
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f8f9fa;
    color: #007bff;
  }
`;

const NavIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SidebarFooter = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  border-top: 1px solid #e9ecef;
`;

const LogoutButton = styled.button`
  width: 100%;
  padding: 12px 20px;
  border: none;
  background: transparent;
  color: #dc3545;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f8f9fa;
  }
`;

const Overlay = styled.div<{ isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: ${props => props.isOpen ? 'block' : 'none'};
  
  @media (min-width: 769px) {
    display: none;
  }
`;

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', icon: BarChart3, label: 'Дашборд' },
    { path: '/users', icon: Users, label: 'Пользователи' },
    { path: '/funds', icon: Building2, label: 'Фонды' },
    { path: '/campaigns', icon: Target, label: 'Кампании' },
    { path: '/reports', icon: FileText, label: 'Отчеты' },
    { path: '/settings', icon: Settings, label: 'Настройки' },
  ];

  const handleLogout = () => {
    // Логика выхода
    console.log('Logout');
  };

  return (
    <>
      <Overlay isOpen={isOpen} onClick={onClose} />
      <SidebarContainer isOpen={isOpen}>
        <SidebarHeader>
          <Logo>
            <BarChart3 size={24} />
            Sadaka-Pass Admin
          </Logo>
        </SidebarHeader>
        
        <SidebarNav>
          <NavList>
            {menuItems.map((item) => (
              <NavItem key={item.path}>
                <NavLink
                  active={location.pathname === item.path}
                  onClick={() => {
                    navigate(item.path);
                    onClose();
                  }}
                >
                  <NavIcon>
                    <item.icon size={16} />
                  </NavIcon>
                  {item.label}
                </NavLink>
              </NavItem>
            ))}
          </NavList>
        </SidebarNav>
        
        <SidebarFooter>
          <LogoutButton onClick={handleLogout}>
            <NavIcon>
              <LogOut size={16} />
            </NavIcon>
            Выйти
          </LogoutButton>
        </SidebarFooter>
      </SidebarContainer>
    </>
  );
};

export default Sidebar;
