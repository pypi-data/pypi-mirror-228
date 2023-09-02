import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import magic
import PyPDF2
from sklearn.preprocessing import LabelEncoder


class Eda:
    def __init__(self, file_path, target_column, threshold=1.5):
        self.file_path=file_path
        self.col=target_column
        self.threshold=threshold
        mime = magic.Magic()
        self.file_type = mime.from_file(self.file_path)
        print('Sucessfull Installation of pacakge')

    def reading(self):
        if "PDF" in self.file_type:
            with open(self.file_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                text = ""
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    text += page.extractText()
            return text
        
        elif "CSV" in self.file_type:
            csv_df = pd.read_csv(self.file_path)
            return csv_df
        elif "Microsoft Excel" in self.file_type:
            excel_df = pd.read_excel(self.file_path)
            return excel_df
        else:
            return "Unsupported file type."


    def outlier_detection(self):
        data=self.reading()
        if data is None:
            return None

        # Checking whether the column is available are not
        if self.col not in data.columns:
            return "provided traget column is not available" 

        # Calculate IQR for the target column
        Q1 = data[self.col].quantile(0.25)
        Q3 = data[self.col].quantile(0.75)
        IQR = Q3 - Q1

        # Define the upper and lower bounds for outlier removal
        lower_bound = Q1 - self.threshold * IQR
        upper_bound = Q3 + self.threshold * IQR

        # Remove outliers from the dataset
        filtered_data = data[(data[self.col] >= lower_bound) & (data[self.col] <= upper_bound)]

        return filtered_data

    
    def replace_nan(self):
        replaced_data = self.outlier_detection()
        for column in replaced_data.columns:
            if replaced_data[column].dtype in ['int', 'float']:
                replaced_data[column].fillna(replaced_data[column].median(), inplace=True)
            else:
                replaced_data[column].fillna(replaced_data[column].mode().iloc[0], inplace=True)
        return replaced_data


            
    def plotting(self):
        # Assuming target column is numerical.
        data= self.replace_nan()
        string_data=data.select_dtypes(include=['object','category'])
        string_data['Target_column']=data[self.col]
        correlated_df= data.select_dtypes(include=['int', 'float'])
        corr_data=pd.DataFrame(correlated_df.corr()[self.col])
        # col_names= corr_data[0.1 < corr_data[self.col] < 0.7].index.tolist()
        # neat_df=data[[col_names]]
        # Filter columns based on correlation condition
        col_names = corr_data[(corr_data[self.col] > 0.1) & (corr_data[self.col] < 0.7)].index.tolist()
        neat_df = data[col_names]

        # full_df=pd.concat([neat_df,string_data], axis=1)
        
        for col in neat_df.columns:
            if neat_df[col].dtype in ['int', 'float']:
                plt.scatter(neat_df[col], data[self.col])
                plt.xlabel(col)
                plt.ylabel(self.col)
                plt.title(f'Scatter plot of {col} vs {self.col}')
                plt.show()
        
        # Categorical columns
        for col in string_data.columns:
            if string_data[col].dtype == 'object':
                grouped_data = data.groupby(col)[self.col].mean()
                plt.bar(grouped_data.index, grouped_data.values)
                plt.xlabel(col)
                plt.ylabel(f'Mean {self.col}')
                plt.title(f'Bar plot of Mean {self.col} by {col}')
                plt.xticks(rotation=45)
                plt.show()
        return plt.show()

