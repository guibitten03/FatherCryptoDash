def get_amount_coins(line_filtered_df):
    amout_buyed = line_filtered_df.loc[line_filtered_df['Status'] == "Buy"]['Qte']
    amout_sold = line_filtered_df.loc[line_filtered_df['Status'] == "Sell"]['Qte']
    amount_reinvested = line_filtered_df.loc[line_filtered_df['Status'] == "Rebuy"]['Qte']

    if len(amout_buyed): amout_buyed = amout_buyed.sum() 
    else: amout_buyed = 0.0      

    if len(amout_sold): amout_sold = amout_sold.sum() 
    else: amout_sold = 0.0   

    if len(amount_reinvested): amount_reinvested = amount_reinvested.sum() 
    else: amount_reinvested = 0.0     

    total_amount = amout_buyed + amount_reinvested - amout_sold
    return total_amount