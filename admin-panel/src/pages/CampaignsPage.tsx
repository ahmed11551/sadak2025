import React from 'react';
import styled from 'styled-components';
import { Target, CheckCircle, Clock, XCircle, TrendingUp } from 'lucide-react';

const CampaignsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageTitle = styled.h2`
  font-size: 24px;
  font-weight: 600;
  color: #212529;
  margin-bottom: 24px;
`;

const Content = styled.div`
  background: #ffffff;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
`;

const Icon = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: #6c757d;
`;

const Title = styled.h3`
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #212529;
`;

const Description = styled.p`
  font-size: 16px;
  color: #6c757d;
  margin-bottom: 24px;
`;

const FeaturesList = styled.div`
  text-align: left;
  max-width: 400px;
  margin: 0 auto;
`;

const FeatureItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  font-size: 14px;
  color: #6c757d;
`;

const FeatureIcon = styled.div<{ color: string }>`
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
`;

const CampaignsPage: React.FC = () => {
  const features = [
    { text: 'Модерация созданных кампаний', icon: CheckCircle, color: '#28a745' },
    { text: 'Управление статусами кампаний', icon: Clock, color: '#ffc107' },
    { text: 'Мониторинг прогресса сбора', icon: TrendingUp, color: '#007bff' },
    { text: 'Управление категориями кампаний', icon: Target, color: '#6c757d' },
    { text: 'Отклонение неподходящих кампаний', icon: XCircle, color: '#dc3545' },
  ];

  return (
    <CampaignsContainer>
      <PageTitle>Кампании</PageTitle>
      <Content>
        <Icon>
          <Target size={40} />
        </Icon>
        <Title>Управление кампаниями</Title>
        <Description>
          Здесь будет интерфейс для модерации пользовательских кампаний, 
          управления их статусами и мониторинга прогресса сбора средств.
        </Description>
        <FeaturesList>
          {features.map((feature, index) => (
            <FeatureItem key={index}>
              <FeatureIcon color={feature.color}>
                <feature.icon size={12} />
              </FeatureIcon>
              {feature.text}
            </FeatureItem>
          ))}
        </FeaturesList>
      </Content>
    </CampaignsContainer>
  );
};

export default CampaignsPage;
