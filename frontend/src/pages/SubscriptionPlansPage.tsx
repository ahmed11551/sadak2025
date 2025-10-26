import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { 
  Crown, 
  ArrowLeft, 
  Check, 
  Star, 
  Heart,
  Gift,
  TrendingUp,
  Shield,
  Users,
  Zap
} from 'lucide-react';
import toast from 'react-hot-toast';
import telegramService from '../services/telegram';

const SubscriptionContainer = styled.div`
  padding: 20px 16px;
  max-width: 100%;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
`;

const BackButton = styled.button`
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--tg-text-color, #000000);
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

const PlansGrid = styled.div`
  display: grid;
  gap: 20px;
  margin-bottom: 32px;
`;

const PlanCard = styled.div<{ featured?: boolean }>`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.2s ease;
  
  ${props => props.featured && `
    border: 2px solid var(--tg-button-color, #007bff);
    transform: scale(1.05);
  `}
  
  &:hover {
    transform: ${props => props.featured ? 'scale(1.05)' : 'translateY(-4px)'};
  }
`;

const FeaturedBadge = styled.div`
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
`;

const PlanHeader = styled.div`
  text-align: center;
  margin-bottom: 24px;
`;

const PlanIcon = styled.div<{ color: string }>`
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
`;

const PlanName = styled.h3`
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--tg-text-color, #000000);
`;

const PlanDescription = styled.p`
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 16px;
`;

const PlanPrice = styled.div`
  margin-bottom: 20px;
`;

const PriceAmount = styled.div`
  font-size: 32px;
  font-weight: 700;
  color: var(--tg-text-color, #000000);
  margin-bottom: 4px;
`;

const PricePeriod = styled.div`
  font-size: 14px;
  color: #6c757d;
`;

const CharityInfo = styled.div`
  background: #f8f9fa;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 20px;
  text-align: center;
`;

const CharityText = styled.div`
  font-size: 14px;
  color: #28a745;
  font-weight: 500;
`;

const FeaturesList = styled.ul`
  list-style: none;
  padding: 0;
  margin-bottom: 24px;
`;

const FeatureItem = styled.li`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  font-size: 14px;
  color: var(--tg-text-color, #000000);
`;

const FeatureIcon = styled.div`
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #28a745;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
`;

const PlanButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  
  ${props => props.variant === 'primary' ? `
    background: var(--tg-button-color, #007bff);
    color: var(--tg-button-text-color, #ffffff);
  ` : `
    background: #f8f9fa;
    color: var(--tg-text-color, #000000);
    border: 2px solid #e9ecef;
  `}
  
  &:hover {
    opacity: 0.9;
  }
`;

const PeriodSelector = styled.div`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const PeriodTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--tg-text-color, #000000);
`;

const PeriodOptions = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
`;

const PeriodOption = styled.button<{ selected: boolean }>`
  padding: 16px;
  border: 2px solid ${props => props.selected ? 'var(--tg-button-color, #007bff)' : '#e9ecef'};
  border-radius: 12px;
  background: ${props => props.selected ? 'var(--tg-button-color, #007bff)' : 'transparent'};
  color: ${props => props.selected ? 'var(--tg-button-text-color, #ffffff)' : 'var(--tg-text-color, #000000)'};
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
`;

const PeriodName = styled.div`
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
`;

const PeriodPrice = styled.div`
  font-size: 14px;
  opacity: 0.8;
`;

const PeriodDiscount = styled.div`
  font-size: 12px;
  color: #28a745;
  font-weight: 500;
`;

const InfoSection = styled.div`
  background: #f8f9fa;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
`;

const InfoTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--tg-text-color, #000000);
`;

const InfoText = styled.p`
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
  margin-bottom: 8px;
`;

const SubscriptionPlansPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedPeriod, setSelectedPeriod] = useState<'1M' | '3M' | '6M' | '12M'>('1M');

  const plans = [
    {
      id: 'basic',
      name: 'Базовый',
      description: 'Для начинающих в благотворительности',
      icon: <Heart size={32} />,
      color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      charityPercentage: 0,
      features: [
        'Доступ к базовым кампаниям',
        'История пожертвований',
        'Уведомления о новых кампаниях',
        'Поддержка по Telegram'
      ],
      prices: {
        '1M': 290,
        '3M': 870,
        '6M': 1160,
        '12M': 2320
      }
    },
    {
      id: 'pro',
      name: 'Pro',
      description: 'Для активных участников сообщества',
      icon: <TrendingUp size={32} />,
      color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      charityPercentage: 5,
      featured: true,
      features: [
        'Все возможности Базового',
        'Приоритетная поддержка',
        'Ранний доступ к кампаниям',
        'Детальная аналитика',
        '5% от подписки в благотворительность'
      ],
      prices: {
        '1M': 590,
        '3M': 1770,
        '6M': 2360,
        '12M': 4720
      }
    },
    {
      id: 'premium',
      name: 'Premium',
      description: 'Максимальная поддержка уммы',
      icon: <Crown size={32} />,
      color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      charityPercentage: 10,
      features: [
        'Все возможности Pro',
        'Персональный менеджер',
        'Эксклюзивные кампании',
        'VIP статус в сообществе',
        '10% от подписки в благотворительность',
        'Приоритет в модерации кампаний'
      ],
      prices: {
        '1M': 990,
        '3M': 2970,
        '6M': 3960,
        '12M': 7920
      }
    }
  ];

  const periodInfo = {
    '1M': { name: '1 месяц', discount: null },
    '3M': { name: '3 месяца', discount: null },
    '6M': { name: '6 месяцев', discount: '+2 мес в подарок' },
    '12M': { name: '12 месяцев', discount: '+4 мес в подарок' }
  };

  const handlePlanSelect = (planId: string) => {
    telegramService.hapticFeedback('impact', 'medium');
    
    // Здесь будет логика выбора плана и перехода к оплате
    toast.success(`Выбран план ${planId} на ${periodInfo[selectedPeriod].name}`);
    console.log('Selected plan:', planId, 'Period:', selectedPeriod);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
  };

  return (
    <SubscriptionContainer>
      <Header>
        <BackButton onClick={() => navigate('/')}>
          <ArrowLeft size={24} />
        </BackButton>
        <div>
          <Title>Садака-подписка</Title>
          <Subtitle>Регулярная милостыня для развития цифровой уммы</Subtitle>
        </div>
      </Header>

      <PeriodSelector>
        <PeriodTitle>Выберите период подписки</PeriodTitle>
        <PeriodOptions>
          {Object.entries(periodInfo).map(([key, info]) => (
            <PeriodOption
              key={key}
              selected={selectedPeriod === key}
              onClick={() => setSelectedPeriod(key as any)}
            >
              <PeriodName>{info.name}</PeriodName>
              <PeriodPrice>
                {formatPrice(plans[1].prices[key as keyof typeof plans[1].prices])}
              </PeriodPrice>
              {info.discount && (
                <PeriodDiscount>
                  <Gift size={12} style={{ marginRight: '4px' }} />
                  {info.discount}
                </PeriodDiscount>
              )}
            </PeriodOption>
          ))}
        </PeriodOptions>
      </PeriodSelector>

      <PlansGrid>
        {plans.map((plan) => (
          <PlanCard key={plan.id} featured={plan.featured}>
            {plan.featured && (
              <FeaturedBadge>
                <Star size={12} />
                Рекомендуем
              </FeaturedBadge>
            )}
            
            <PlanHeader>
              <PlanIcon color={plan.color}>
                {plan.icon}
              </PlanIcon>
              <PlanName>{plan.name}</PlanName>
              <PlanDescription>{plan.description}</PlanDescription>
            </PlanHeader>

            <PlanPrice>
              <PriceAmount>
                {formatPrice(plan.prices[selectedPeriod])}
              </PriceAmount>
              <PricePeriod>за {periodInfo[selectedPeriod].name.toLowerCase()}</PricePeriod>
            </PlanPrice>

            {plan.charityPercentage > 0 && (
              <CharityInfo>
                <CharityText>
                  <Heart size={14} style={{ marginRight: '4px' }} />
                  {plan.charityPercentage}% от подписки идет в благотворительность
                </CharityText>
              </CharityInfo>
            )}

            <FeaturesList>
              {plan.features.map((feature, index) => (
                <FeatureItem key={index}>
                  <FeatureIcon>
                    <Check size={12} />
                  </FeatureIcon>
                  {feature}
                </FeatureItem>
              ))}
            </FeaturesList>

            <PlanButton
              variant={plan.featured ? 'primary' : 'secondary'}
              onClick={() => handlePlanSelect(plan.id)}
            >
              {plan.featured ? <Crown size={16} /> : <Zap size={16} />}
              {plan.featured ? 'Выбрать Pro' : `Выбрать ${plan.name}`}
            </PlanButton>
          </PlanCard>
        ))}
      </PlansGrid>

      <InfoSection>
        <InfoTitle>Что такое садака-подписка?</InfoTitle>
        <InfoText>
          Садака-подписка — это ваша регулярная милостыня (садака-джария) на развитие цифровой уммы.
        </InfoText>
        <InfoText>
          Получайте доступ к знаниям, участвуйте в эксклюзивных кампаниях и получайте благодарность за вашу поддержку.
        </InfoText>
        <InfoText>
          Часть средств от Pro и Premium подписок автоматически перечисляется в благотворительные фонды.
        </InfoText>
      </InfoSection>

      <InfoSection>
        <InfoTitle>Преимущества подписки</InfoTitle>
        <InfoText>
          • Доступ к эксклюзивному контенту и кампаниям
        </InfoText>
        <InfoText>
          • Приоритетная поддержка и персональный менеджер
        </InfoText>
        <InfoText>
          • Детальная аналитика ваших пожертвований
        </InfoText>
        <InfoText>
          • VIP статус в сообществе благотворителей
        </InfoText>
        <InfoText>
          • Автоматическое участие в садака-джария
        </InfoText>
      </InfoSection>
    </SubscriptionContainer>
  );
};

export default SubscriptionPlansPage;
