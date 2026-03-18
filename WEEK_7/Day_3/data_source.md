# Data Source

I used an AI Jobs Market dataset (15,000 job postings) instead of the generated evaluation data from the lab script. This dataset contains salary, experience level, employment type, remote ratio, industry, and company size fields across AI-related roles globally.

The dataset maps directly to the lab requirements: `salary_usd` serves as the numeric metric (equivalent to evaluation scores), and `experience_level` and `remote_ratio` serve as the primary analytical categories (equivalent to evaluation categories). Both were used as dedicated chart dimensions in the dashboard.

This data was chosen because it is richer than the generated sample data, produces more meaningful visualizations, and tells a compelling real-world story relevant to AI consulting.
