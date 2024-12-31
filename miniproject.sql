#1 Total Expenditure
Select sum(Amount_Paid) as Total_Expenditure
From allmonths

#2 Most Expensive Transaction
Select * 
From allmonths
order by Amount_Paid desc
limit 1

#3 Monthly Expenditure Breakdown
Select 
	Month(Date) as Month,
    Sum(Amount_Paid) as Monthly_Expenditure
From allmonths
Group by Month(Date)
Order by month

#4 Top Spending Categories
Select
	 Category,
     Sum(Amount_Paid) as Total_Spent
From allmonths
group by Category
order by Total_Spent desc

#5 Payment Mode Distribution
Select
	Month(Date) as Month,
    Sum(Cashback) as Total_Cashback
From Allmonths
Group by Month(Date)
Order by Month

#6 Average Spend per Transaction
Select 
	avg(Amount_Paid) as Average_Transaction_Amount
From Allmonths

#7 Categories with Cashback Opprtunities
Select 
	Category,
    Sum(Cashback) as Total_Cashback
From Allmonths
Group by Category
Order by Total_Cashback desc

#8 Least Spending Categories
Select 
	Category,
    Sum(Amount_Paid) as Total_Spent
From Allmonths
Group by Category
Order by Total_Spent ASC
Limit 1

#9 Average monthly Cashback
Select 
	Month(Date) as Month,
    Avg(Cashback) as Avg_Cashback
From Allmonths
Group by month(date)

#10 Daily Spending Trends
Select 
	day(date) as day,
    sum(Amount_Paid) as Total_Spent
From allmonths
group by day(date)
order by day

#11 Month with Maximum Expenditure
Select
	month(date) as Month,
    sum(Amount_Paid) as Total_Expenditure
From allmonths
Group by month(date)
order by Total_Expenditure desc
Limit 1

#12 Maximum and Minimum Transaction amounts
Select
	max(Amount_Paid) as Max_Transaction,
    min(Amount_Paid) as Min_Transaction
From allmonths

#13 Cashback earned by month
Select
	month(date) as month,
    Sum(Cashback) as Total_Cashback
From allmonths
group by month(date)
order by month

#14 Transactions exceeding amount 490
Select *
From allmonths
where Amount_Paid > 490

#15 Average transaction amount by category
Select 
	Category,
    Avg(Amount_Paid) as Avg_Transaction_Amount
From allmonths
group by Category