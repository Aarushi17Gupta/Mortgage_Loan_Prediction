# save this as app.py
from flask import Flask, request, render_template
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
model = pickle.load(open('model_knn.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("Contact.html")

@app.route('/about')
def about():
    return render_template("AboutUs.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        occupancy = request.form['occupancy']
        Property = request.form['Property']
        Channel = request.form['Channel']
        purpose = request.form['purpose']
        num_borrow = request.form['num_borrow']
        Units = float(request.form['Units'])
        CS = float(request.form['CS'])
        MIP = float(request.form['MIP'])
        OCLTV = float(request.form['OCLTV'])
        DTI = float(request.form['DTI'])
        OrigUPB = float(request.form['OrigUPB'])
        int_rate = float(request.form['int_rate'])
        months_repayment = float(request.form['months_repayment'])
        
        years_repayment = months_repayment/12
        
        CS_log = np.log(CS+1)
        MIP_log = np.log(MIP+1)
        OCLTV_log = np.log(OCLTV+1)
        DTI_log = np.log(DTI+1)
        OrigUPB_log = np.log(OrigUPB+1)
        int_rate_log = np.log(int_rate+1)
        years_repayment_log = np.log(years_repayment+1)

        if (CS >= 0) & (CS < 650):
            CreditRange = 'Poor'
        elif (CS >= 650) & (CS < 700):
            CreditRange = 'Fair'
        elif (CS >= 700) & (CS < 750):
            CreditRange = 'Good'
        elif (CS >= 750):
            CreditRange = 'Excellent'

        
        if (years_repayment >= 0) & (years_repayment <4):
            RepayRange = '0-4yrs'
        elif (years_repayment >= 4) & (years_repayment <10):
            RepayRange = '4-10yrs'
        elif (years_repayment >= 10) & (years_repayment <15):
            RepayRange = '10-15yrs'
        elif (years_repayment >= 15):
            RepayRange = '15-20yrs'


        if (OCLTV >= 0) & (OCLTV < 45):
            LTVRange = 'Low'
        elif (OCLTV >= 45) & (OCLTV < 80):
            LTVRange = 'Medium'
        elif (OCLTV >= 80):
            LTVRange = 'High'        

        
        if (CreditRange == 'Poor'):
            CreditRange_Fair = 0
            CreditRange_Good = 0
            CreditRange_Poor = 1
        elif (CreditRange == 'Fair'):
            CreditRange_Fair = 1
            CreditRange_Good = 0
            CreditRange_Poor = 0
        elif (CreditRange == 'Good'):
            CreditRange_Fair = 0
            CreditRange_Good = 1
            CreditRange_Poor = 0
        else:
            CreditRange_Fair = 0
            CreditRange_Good = 0
            CreditRange_Poor = 0
    
        if (RepayRange == '0-4yrs'):
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 0
        elif (RepayRange == '4-10yrs'):
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 1
        elif (RepayRange == '10-15yrs'):
            Repay_range_in_years_10_15yrs = 1
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 0
        else:
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 1
            Repay_range_in_years_4_10yrs = 0
    

        if (LTVRange == 'Low'):
            LTV_range_Low = 1
            LTV_range_Medium = 0
        elif (LTVRange == 'Medium'):
            LTV_range_Low = 0
            LTV_range_Medium = 1
        else:
            LTV_range_Low = 0
            LTV_range_Medium = 0


        prediction = model.predict([[CS_log, MIP_log, Units, OCLTV_log, DTI_log, OrigUPB_log, int_rate_log, years_repayment_log,\
                             Repay_range_in_years_10_15yrs, Repay_range_in_years_15_20yrs, Repay_range_in_years_4_10yrs,\
                             CreditRange_Fair, CreditRange_Good, CreditRange_Poor, LTV_range_Low, LTV_range_Medium]])

        # print(prediction)

        if(prediction[0]==1):
            prediction="Yes"
        else:
            prediction="No"


        return render_template("Prediction.html", prediction_text="Applicant chances for Defaulting :-{}".format(prediction))




    else:
        return render_template("Prediction.html")



if __name__ == "__main__":
    app.run(debug=True)
    