import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { 
  Heart, 
  Calculator, 
  Users, 
  FileText, 
  TrendingUp,
  Shield,
  Clock,
  Star,
  Target
} from 'lucide-react';
import telegramService from '../services/telegram.ts';

const HomeContainer = styled.div`
  padding: 20px 16px;
  max-width: 100%;
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 32px;
`;

const Title = styled.h1`
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--tg-text-color, #000000);
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: #6c757d;
  margin-bottom: 24px;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 32px;
`;

const StatCard = styled.div`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const StatIcon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: white;
`;

const StatValue = styled.div`
  font-size: 24px;
  font-weight: 700;
  color: var(--tg-text-color, #000000);
  margin-bottom: 4px;
`;

const StatLabel = styled.div`
  font-size: 14px;
  color: #6c757d;
`;

const ActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 32px;
`;

const ActionCard = styled.div`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  }
`;

const ActionIcon = styled.div<{ color: string }>`
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
`;

const ActionTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--tg-text-color, #000000);
`;

const ActionDescription = styled.p`
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
`;

const QuickActions = styled.div`
  margin-bottom: 32px;
`;

const QuickActionsTitle = styled.h2`
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--tg-text-color, #000000);
`;

const QuickActionButton = styled.button`
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: var(--tg-button-color, #007bff);
  color: var(--tg-button-text-color, #ffffff);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
  
  &:hover {
    opacity: 0.9;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const FeaturesSection = styled.div`
  margin-bottom: 32px;
`;

const FeaturesTitle = styled.h2`
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--tg-text-color, #000000);
`;

const FeatureItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #e9ecef;
  
  &:last-child {
    border-bottom: none;
  }
`;

const FeatureIcon = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #007bff;
`;

const FeatureText = styled.span`
  font-size: 16px;
  color: var(--tg-text-color, #000000);
`;

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleActionClick = (action: string) => {
    telegramService.hapticFeedback('impact', 'light');
    
    switch (action) {
      case 'donate':
        navigate('/funds');
        break;
      case 'zakat':
        navigate('/zakat');
        break;
      case 'subscription':
        navigate('/funds');
        break;
      case 'partner':
        navigate('/partner');
        break;
    }
  };

  return (
    <HomeContainer>
      <Header>
        <Title>🕌 Sadaka-Pass</Title>
        <Subtitle>
          Платформа для пожертвований и расчета закята
        </Subtitle>
      </Header>

      <StatsGrid>
        <StatCard>
          <StatIcon>
            <Heart size={24} />
          </StatIcon>
          <StatValue>1,247</StatValue>
          <StatLabel>Пожертвований</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon>
            <Users size={24} />
          </StatIcon>
          <StatValue>89</StatValue>
          <StatLabel>Фондов</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon>
            <TrendingUp size={24} />
          </StatIcon>
          <StatValue>₽2.4M</StatValue>
          <StatLabel>Собрано</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon>
            <Shield size={24} />
          </StatIcon>
          <StatValue>100%</StatValue>
          <StatLabel>Прозрачность</StatLabel>
        </StatCard>
      </StatsGrid>

      <ActionsGrid>
        <ActionCard onClick={() => handleActionClick('donate')}>
          <ActionIcon color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
            <Heart size={28} />
          </ActionIcon>
          <ActionTitle>Разовое пожертвование</ActionTitle>
          <ActionDescription>
            Поддержать конкретную цель или проект
          </ActionDescription>
        </ActionCard>

        <ActionCard onClick={() => handleActionClick('zakat')}>
          <ActionIcon color="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
            <Calculator size={28} />
          </ActionIcon>
          <ActionTitle>Калькулятор закята</ActionTitle>
          <ActionDescription>
            Рассчитать и оплатить закят
          </ActionDescription>
        </ActionCard>

        <ActionCard onClick={() => navigate('/subscription-plans')}>
          <ActionIcon color="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
            <Clock size={28} />
          </ActionIcon>
          <ActionTitle>Садака-подписка</ActionTitle>
          <ActionDescription>
            Регулярная милостыня с тарифами
          </ActionDescription>
        </ActionCard>

        <ActionCard onClick={() => navigate('/campaigns')}>
          <ActionIcon color="linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)">
            <Target size={28} />
          </ActionIcon>
          <ActionTitle>Целевые кампании</ActionTitle>
          <ActionDescription>
            Создание и участие в кампаниях
          </ActionDescription>
        </ActionCard>

        <ActionCard onClick={() => handleActionClick('partner')}>
          <ActionIcon color="linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
            <FileText size={28} />
          </ActionIcon>
          <ActionTitle>Стать партнером</ActionTitle>
          <ActionDescription>
            Подать заявку на партнерство
          </ActionDescription>
        </ActionCard>
      </ActionsGrid>

      <QuickActions>
        <QuickActionsTitle>Быстрые действия</QuickActionsTitle>
        <QuickActionButton onClick={() => handleActionClick('donate')}>
          <Heart size={20} />
          Сделать пожертвование
        </QuickActionButton>
        <QuickActionButton onClick={() => handleActionClick('zakat')}>
          <Calculator size={20} />
          Рассчитать закят
        </QuickActionButton>
      </QuickActions>

      <FeaturesSection>
        <FeaturesTitle>Преимущества платформы</FeaturesTitle>
        <FeatureItem>
          <FeatureIcon>
            <Shield size={16} />
          </FeatureIcon>
          <FeatureText>100% прозрачность использования средств</FeatureText>
        </FeatureItem>
        <FeatureItem>
          <FeatureIcon>
            <Star size={16} />
          </FeatureIcon>
          <FeatureText>Верифицированные благотворительные фонды</FeatureText>
        </FeatureItem>
        <FeatureItem>
          <FeatureIcon>
            <TrendingUp size={16} />
          </FeatureIcon>
          <FeatureText>Отчеты о достигнутых результатах</FeatureText>
        </FeatureItem>
        <FeatureItem>
          <FeatureIcon>
            <Users size={16} />
          </FeatureIcon>
          <FeatureText>Сообщество единомышленников</FeatureText>
        </FeatureItem>
      </FeaturesSection>
    </HomeContainer>
  );
};

export default HomePage;
