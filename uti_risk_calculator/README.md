# UTI Risk Calculator

A web-based clinical decision support tool for predicting the risk of Urinary Tract Infection (UTI) using a LASSO regression model.

## Overview

This calculator provides healthcare professionals with a simple, accurate way to estimate a patient's risk of UTI based on clinical parameters. The underlying model was developed using LASSO regression and validated with a dataset of patients, achieving an AUC of 0.805 (95% CI: 0.771-0.839) in the validation set.

## Features

- Simple, intuitive web interface
- Real-time risk calculation
- Visual risk indicators and interpretations
- Responsive design for desktop and mobile devices
- No server-side processing (all calculations performed in the browser)

## How to Use

1. Open `index.html` in any modern web browser
2. Enter the required patient data:
   - Age
   - Sex
   - BMI
   - NPAR
   - Urine Leukocyte Esterase status
   - Urinary Nitrite status
   - Hydronephrosis status
   - White Blood Cell Count
   - Occult Blood in Urine status
3. Click "Calculate Risk"
4. Review the results, which include:
   - UTI risk probability as a percentage
   - Risk category (Low, Moderate, High)
   - Clinical interpretation

## Model Details

The calculator uses a LASSO (Least Absolute Shrinkage and Selection Operator) regression model with the following features:

| Feature | Coefficient |
|---------|-------------|
| Intercept | -2.0126 |
| Urine Leukocyte Esterase | 0.7971 |
| Urinary Nitrite | 0.3497 |
| Hydronephrosis | -0.2556 |
| BMI | 0.2001 |
| Age | 0.1963 |
| White Blood Cell Count | -0.1932 |
| NPAR | 0.1875 |
| Sex | 0.1864 |

## Technical Implementation

- HTML5, CSS3, and JavaScript (ES6)
- Bootstrap 5 for responsive layout and styling
- No external dependencies or server requirements
- The model uses a sigmoid function to convert the linear predictor to a probability

## Limitations

This calculator is intended for clinical reference only and should not replace clinical judgment or standard diagnostic procedures. The model was developed and validated on a specific patient population, and its performance may vary in different clinical settings.

## License

For research and educational purposes only.

## Citation

If you use this calculator in your research, please cite:

```
[Citation information would be placed here]
``` 