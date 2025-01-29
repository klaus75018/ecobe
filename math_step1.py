from polls.models import PrincingDBProjectSubPricingSubTradeCompanyOffer

#somme des offfres

for i in PrincingDBProjectSubPricingSubTradeCompanyOffer.objects.all():
    print(i)
    tot = 0.0
    for j in i.princingdbprojectsubpricingsubsubtradegroup_set.all():
        totint = j.group_price
        tot = tot + totint
        print(tot)
    i.company_offer_sub_trade_price = tot
    i.save()