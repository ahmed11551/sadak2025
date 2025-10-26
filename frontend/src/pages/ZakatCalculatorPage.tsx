import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useForm } from 'react-hook-form';
import { Calculator, DollarSign, Minus, Plus, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import telegramService from '../services/telegram';
import { zakatApi } from '../services/api';
import { ZakatCalculationCreate } from '../types';

const ZakatContainer = styled.div`
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

const FormSection = styled.div`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const SectionTitle = styled.h2`
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--tg-text-color, #000000);
  display: flex;
  align-items: center;
  gap: 12px;
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  margin-bottom: 16px;
`;

const FormLabel = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--tg-text-color, #000000);
  font-size: 14px;
`;

const FormInput = styled.input`
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  
  &:focus {
    outline: none;
    border-color: var(--tg-button-color, #007bff);
  }
  
  &::placeholder {
    color: #6c757d;
  }
`;

const InputGroup = styled.div`
  position: relative;
`;

const InputIcon = styled.div`
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 18px;
`;

const InputWithIcon = styled(FormInput)`
  padding-left: 40px;
`;

const SummaryCard = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  margin-bottom: 24px;
`;

const SummaryTitle = styled.h3`
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  text-align: center;
`;

const SummaryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
`;

const SummaryItem = styled.div`
  text-align: center;
`;

const SummaryLabel = styled.div`
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 4px;
`;

const SummaryValue = styled.div`
  font-size: 18px;
  font-weight: 600;
`;

const ZakatAmount = styled.div`
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-bottom: 20px;
`;

const ZakatAmountLabel = styled.div`
  font-size: 16px;
  opacity: 0.8;
  margin-bottom: 8px;
`;

const ZakatAmountValue = styled.div`
  font-size: 32px;
  font-weight: 700;
`;

const ZakatFormula = styled.div`
  font-size: 14px;
  opacity: 0.8;
  text-align: center;
`;

const ActionButton = styled.button`
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: var(--tg-button-color, #007bff);
  color: var(--tg-button-text-color, #ffffff);
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  
  &:hover {
    opacity: 0.9;
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const InfoCard = styled.div`
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
`;

const InfoTitle = styled.h4`
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--tg-text-color, #000000);
`;

const InfoText = styled.p`
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
`;

const Checkbox = styled.input`
  margin-top: 2px;
`;

const CheckboxLabel = styled.label`
  font-size: 14px;
  color: var(--tg-text-color, #000000);
  line-height: 1.4;
`;

const ZakatCalculatorPage: React.FC = () => {
  const navigate = useNavigate();
  const [isCalculating, setIsCalculating] = useState(false);
  const [isPaying, setIsPaying] = useState(false);
  const [calculation, setCalculation] = useState<any>(null);
  const [nisab, setNisab] = useState(952389);
  const [acceptedTerms, setAcceptedTerms] = useState(false);

  const { register, handleSubmit, watch, formState: { errors } } = useForm<ZakatCalculationCreate>({
    defaultValues: {
      cash_at_home: 0,
      bank_accounts: 0,
      shares_value: 0,
      goods_profit: 0,
      gold_silver_value: 0,
      property_investments: 0,
      other_income: 0,
      debts: 0,
      expenses: 0,
    }
  });

  const watchedValues = watch();

  useEffect(() => {
    // Получаем текущий нисаб
    const fetchNisab = async () => {
      try {
        const response = await zakatApi.getCurrentNisab();
        setNisab(response.data.nisab_amount);
      } catch (error) {
        console.error('Error fetching nisab:', error);
      }
    };

    fetchNisab();
  }, []);

  // Рассчитываем закят в реальном времени
  const calculateZakat = () => {
    const totalAssets = 
      (watchedValues.cash_at_home || 0) +
      (watchedValues.bank_accounts || 0) +
      (watchedValues.shares_value || 0) +
      (watchedValues.goods_profit || 0) +
      (watchedValues.gold_silver_value || 0) +
      (watchedValues.property_investments || 0) +
      (watchedValues.other_income || 0);

    const totalLiabilities = (watchedValues.debts || 0) + (watchedValues.expenses || 0);
    const zakatableAmount = totalAssets - totalLiabilities;
    const zakatAmount = zakatableAmount > nisab ? zakatableAmount * 0.025 : 0;

    return {
      totalAssets,
      totalLiabilities,
      zakatableAmount,
      zakatAmount,
      exceedsNisab: zakatableAmount > nisab
    };
  };

  const currentCalculation = calculateZakat();

  const onSubmit = async (data: ZakatCalculationCreate) => {
    if (!acceptedTerms) {
      toast.error('Необходимо принять условия обработки данных');
      return;
    }

    setIsCalculating(true);
    telegramService.hapticFeedback('impact', 'medium');

    try {
      // Здесь должен быть реальный user_id из Telegram
      const userId = 1; // Mock user ID
      const response = await zakatApi.calculate(userId, data);
      setCalculation(response.data);
      toast.success('Расчет закята выполнен успешно');
    } catch (error) {
      console.error('Error calculating zakat:', error);
      toast.error('Ошибка при расчете закята');
    } finally {
      setIsCalculating(false);
    }
  };

  const handlePayZakat = async () => {
    if (!calculation) return;

    setIsPaying(true);
    telegramService.hapticFeedback('impact', 'medium');

    try {
      const response = await zakatApi.pay(calculation.id, 'yookassa');
      // Здесь должна быть логика перенаправления на платежную страницу
      toast.success('Перенаправление на оплату...');
      console.log('Payment URL:', response.data.payment_url);
    } catch (error) {
      console.error('Error initiating payment:', error);
      toast.error('Ошибка при инициализации платежа');
    } finally {
      setIsPaying(false);
    }
  };

  return (
    <ZakatContainer>
      <Header>
        <Title>🧮 Калькулятор закята</Title>
        <Subtitle>
          Рассчитайте размер закята на основе ваших активов
        </Subtitle>
      </Header>

      <form onSubmit={handleSubmit(onSubmit)}>
        <FormSection>
          <SectionTitle>
            <Plus size={24} />
            Активы
          </SectionTitle>
          
          <FormGrid>
            <FormGroup>
              <FormLabel>Наличные дома</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('cash_at_home', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Остаток на банковских счетах</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('bank_accounts', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Стоимость акций при перепродаже</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('shares_value', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Товары и прибыль</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('goods_profit', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Золото и серебро (по текущей стоимости)</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('gold_silver_value', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Имущество, удерживаемое в качестве инвестиций</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('property_investments', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Другие доходы</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('other_income', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>
          </FormGrid>

          <SummaryItem>
            <SummaryLabel>Общая сумма активов</SummaryLabel>
            <SummaryValue>₽{currentCalculation.totalAssets.toLocaleString()}</SummaryValue>
          </SummaryItem>
        </FormSection>

        <FormSection>
          <SectionTitle>
            <Minus size={24} />
            Обязательства
          </SectionTitle>
          
          <FormGrid>
            <FormGroup>
              <FormLabel>Вычесть долги</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('debts', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>

            <FormGroup>
              <FormLabel>Вычесть расходы</FormLabel>
              <InputGroup>
                <InputIcon>₽</InputIcon>
                <InputWithIcon
                  type="number"
                  step="0.01"
                  placeholder="0"
                  {...register('expenses', { min: 0 })}
                />
              </InputGroup>
            </FormGroup>
          </FormGrid>

          <SummaryItem>
            <SummaryLabel>Общие обязательства</SummaryLabel>
            <SummaryValue>₽{currentCalculation.totalLiabilities.toLocaleString()}</SummaryValue>
          </SummaryItem>
        </FormSection>

        <SummaryCard>
          <SummaryTitle>Результат расчета</SummaryTitle>
          
          <SummaryGrid>
            <SummaryItem>
              <SummaryLabel>Облагаемая закятом сумма</SummaryLabel>
              <SummaryValue>₽{currentCalculation.zakatableAmount.toLocaleString()}</SummaryValue>
            </SummaryItem>
            <SummaryItem>
              <SummaryLabel>Нисаб</SummaryLabel>
              <SummaryValue>₽{nisab.toLocaleString()}</SummaryValue>
            </SummaryItem>
          </SummaryGrid>

          <ZakatAmount>
            <ZakatAmountLabel>Размер закята для выплаты</ZakatAmountLabel>
            <ZakatAmountValue>₽{currentCalculation.zakatAmount.toLocaleString()}</ZakatAmountValue>
            <ZakatFormula>0.025 × облагаемая закятом сумма</ZakatFormula>
          </ZakatAmount>

          {!currentCalculation.exceedsNisab && (
            <InfoCard>
              <InfoTitle>Информация о нисабе</InfoTitle>
              <InfoText>
                Убедитесь, что облагаемая закятом сумма превышает нисаб ({nisab.toLocaleString()} ₽).
                Если сумма меньше нисаба, закят не обязателен.
              </InfoText>
            </InfoCard>
          )}
        </SummaryCard>

        <CheckboxContainer>
          <Checkbox
            type="checkbox"
            checked={acceptedTerms}
            onChange={(e) => setAcceptedTerms(e.target.checked)}
          />
          <CheckboxLabel>
            Принимаю условия обработки персональных данных и условия пожертвования
          </CheckboxLabel>
        </CheckboxContainer>

        <ActionButton
          type="submit"
          disabled={isCalculating || !acceptedTerms}
        >
          <Calculator size={20} />
          {isCalculating ? 'Рассчитываем...' : 'Рассчитать закят'}
        </ActionButton>

        {calculation && calculation.zakat_amount > 0 && (
          <ActionButton
            type="button"
            onClick={handlePayZakat}
            disabled={isPaying}
            style={{ marginTop: '16px', background: '#28a745' }}
          >
            <DollarSign size={20} />
            {isPaying ? 'Обрабатываем...' : 'ОПЛАТИТЬ СВОЙ ЗАКЯТ СЕЙЧАС'}
          </ActionButton>
        )}
      </form>
    </ZakatContainer>
  );
};

export default ZakatCalculatorPage;
