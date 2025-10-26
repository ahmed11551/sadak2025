import React from 'react';
import styled from 'styled-components';
import { 
  Users, 
  Building2, 
  Target, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Activity,
  CreditCard
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

const DashboardContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
`;

const StatCard = styled.div`
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
`;

const StatTitle = styled.h3`
  font-size: 14px;
  font-weight: 500;
  color: #6c757d;
  margin: 0;
`;

const StatIcon = styled.div<{ color: string }>`
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const StatValue = styled.div`
  font-size: 32px;
  font-weight: 700;
  color: #212529;
  margin-bottom: 8px;
`;

const StatChange = styled.div<{ positive: boolean }>`
  font-size: 14px;
  color: ${props => props.positive ? '#28a745' : '#dc3545'};
  display: flex;
  align-items: center;
  gap: 4px;
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ChartCard = styled.div`
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
`;

const ChartTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #212529;
  margin-bottom: 24px;
`;

const RecentActivity = styled.div`
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
`;

const ActivityItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f8f9fa;
  
  &:last-child {
    border-bottom: none;
  }
`;

const ActivityIcon = styled.div<{ color: string }>`
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
`;

const ActivityContent = styled.div`
  flex: 1;
`;

const ActivityText = styled.div`
  font-size: 14px;
  color: #212529;
  margin-bottom: 4px;
`;

const ActivityTime = styled.div`
  font-size: 12px;
  color: #6c757d;
`;

const ActivityAmount = styled.div<{ positive: boolean }>`
  font-size: 14px;
  font-weight: 600;
  color: ${props => props.positive ? '#28a745' : '#dc3545'};
`;

// Mock данные
const donationsData = [
  { month: 'Янв', amount: 240000 },
  { month: 'Фев', amount: 320000 },
  { month: 'Мар', amount: 280000 },
  { month: 'Апр', amount: 450000 },
  { month: 'Май', amount: 380000 },
  { month: 'Июн', amount: 520000 },
];

const fundDistributionData = [
  { name: 'Мечети', value: 35, color: '#007bff' },
  { name: 'Сироты', value: 25, color: '#28a745' },
  { name: 'Медицина', value: 20, color: '#ffc107' },
  { name: 'Образование', value: 15, color: '#dc3545' },
  { name: 'Другое', value: 5, color: '#6c757d' },
];

const recentActivities = [
  {
    icon: DollarSign,
    color: '#28a745',
    text: 'Новое пожертвование в кампанию "Строительство мечети"',
    time: '2 минуты назад',
    amount: '+50,000 ₽',
    positive: true
  },
  {
    icon: Users,
    color: '#007bff',
    text: 'Новый пользователь зарегистрировался',
    time: '15 минут назад',
    amount: '',
    positive: true
  },
  {
    icon: Target,
    color: '#ffc107',
    text: 'Кампания "Помощь сиротам" достигла 80% цели',
    time: '1 час назад',
    amount: '+25,000 ₽',
    positive: true
  },
  {
    icon: Building2,
    color: '#6c757d',
    text: 'Новая заявка на партнерство от фонда "Милосердие"',
    time: '2 часа назад',
    amount: '',
    positive: true
  },
];

const DashboardPage: React.FC = () => {
  const stats = [
    {
      title: 'Всего пользователей',
      value: '3,456',
      change: '+12.5%',
      positive: true,
      icon: Users,
      color: '#007bff'
    },
    {
      title: 'Активных фондов',
      value: '89',
      change: '+3.2%',
      positive: true,
      icon: Building2,
      color: '#28a745'
    },
    {
      title: 'Активных кампаний',
      value: '156',
      change: '+8.1%',
      positive: true,
      icon: Target,
      color: '#ffc107'
    },
    {
      title: 'Собрано за месяц',
      value: '₽2.4M',
      change: '+15.3%',
      positive: true,
      icon: DollarSign,
      color: '#dc3545'
    }
  ];

  return (
    <DashboardContainer>
      <StatsGrid>
        {stats.map((stat, index) => (
          <StatCard key={index}>
            <StatHeader>
              <StatTitle>{stat.title}</StatTitle>
              <StatIcon color={stat.color}>
                <stat.icon size={20} />
              </StatIcon>
            </StatHeader>
            <StatValue>{stat.value}</StatValue>
            <StatChange positive={stat.positive}>
              {stat.positive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              {stat.change}
            </StatChange>
          </StatCard>
        ))}
      </StatsGrid>

      <ChartsGrid>
        <ChartCard>
          <ChartTitle>Динамика пожертвований</ChartTitle>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={donationsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => [`₽${value.toLocaleString()}`, 'Сумма']} />
              <Bar dataKey="amount" fill="#007bff" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard>
          <ChartTitle>Распределение по категориям</ChartTitle>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={fundDistributionData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {fundDistributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}%`, 'Доля']} />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </ChartsGrid>

      <RecentActivity>
        <ChartTitle>Последняя активность</ChartTitle>
        {recentActivities.map((activity, index) => (
          <ActivityItem key={index}>
            <ActivityIcon color={activity.color}>
              <activity.icon size={16} />
            </ActivityIcon>
            <ActivityContent>
              <ActivityText>{activity.text}</ActivityText>
              <ActivityTime>{activity.time}</ActivityTime>
            </ActivityContent>
            {activity.amount && (
              <ActivityAmount positive={activity.positive}>
                {activity.amount}
              </ActivityAmount>
            )}
          </ActivityItem>
        ))}
      </RecentActivity>
    </DashboardContainer>
  );
};

export default DashboardPage;
