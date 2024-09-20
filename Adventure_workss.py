{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "7b783dff",
   "metadata": {},
   "source": [
    "# Importing the sql database into jupyter and establishing connection"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 216,
   "id": "32866843",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tables in the database:                        name\n",
      "0                 FACTsales\n",
      "1              DimCalendars\n",
      "2           sqlite_sequence\n",
      "3      DimProductCategories\n",
      "4  DimProduct_Subcategories\n",
      "5               DimProducts\n",
      "6            DimTerritories\n",
      "7                FACTReturn\n",
      "8               DimCustomer\n",
      "  OrderDate   StockDate OrderNumber  ProductKey  CustomerKey  TerritoryKey  \\\n",
      "0  1/1/2017  12/13/2003     SO61285         529        23791             1   \n",
      "1  1/1/2017   9/24/2003     SO61285         214        23791             1   \n",
      "2  1/1/2017    9/4/2003     SO61285         540        23791             1   \n",
      "3  1/1/2017   9/28/2003     SO61301         529        16747             1   \n",
      "4  1/1/2017  10/21/2003     SO61301         377        16747             1   \n",
      "\n",
      "   OrderLineItem  OrderQuantity  \n",
      "0              2              2  \n",
      "1              3              1  \n",
      "2              1              1  \n",
      "3              2              2  \n",
      "4              1              1  \n"
     ]
    }
   ],
   "source": [
    "import sqlite3\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from scipy import stats\n",
    "import matplotlib.pyplot as plt \n",
    "path = r\"C:\\Users\\alexl\\csv_sql.db\"\n",
    "conn = sqlite3.connect(path)\n",
    "query = \"SELECT name FROM sqlite_master WHERE type='table';\"\n",
    "df_tables = pd.read_sql_query(query, conn)\n",
    "print(\"Tables in the database:\", df_tables)\n",
    "\n",
    "## loading a specific table from the database into a dataframe\n",
    "table_name = 'FACTsales'\n",
    "df = pd.read_sql_query(f\"SELECT * FROM {table_name}\", conn)\n",
    "print(df.head())\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a0794293",
   "metadata": {},
   "source": [
    "## Loading data into a dataframe"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 217,
   "id": "baaaf5f7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "data was suscessfully loaded into Dataframe.\n"
     ]
    }
   ],
   "source": [
    "### these queries loads the the table from the sql database tabes into the pandas dataframe\n",
    "\n",
    "def query_to_dataframe(query):\n",
    "    return pd.read_sql_query(query, conn)\n",
    "\n",
    "FS_df = query_to_dataframe(\"select * from FACTsales\")\n",
    "FR_df = query_to_dataframe(\"select * from FACTReturn\")\n",
    "DP_df = query_to_dataframe(\"select * from DimProducts\")\n",
    "DT_df = query_to_dataframe(\"select * from DimTerritories\")\n",
    "DCAL_df = query_to_dataframe(\"select * from  DimCalendars\")\n",
    "DCU_df = query_to_dataframe(\"select * from  DimCustomer\")\n",
    "DPC_df = query_to_dataframe(\"select * from  DimProductCategories\")\n",
    "DPSC_df = query_to_dataframe(\"select * from  DimProduct_Subcategories\")\n",
    "\n",
    "print(\"data was suscessfully loaded into Dataframe.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "62c1985d",
   "metadata": {},
   "source": [
    "### Data Preprocessing steps"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 218,
   "id": "1f982e99",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>OrderDate</th>\n",
       "      <th>StockDate</th>\n",
       "      <th>OrderNumber</th>\n",
       "      <th>ProductKey</th>\n",
       "      <th>CustomerKey</th>\n",
       "      <th>TerritoryKey</th>\n",
       "      <th>OrderLineItem</th>\n",
       "      <th>OrderQuantity</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1/1/2017</td>\n",
       "      <td>12/13/2003</td>\n",
       "      <td>SO61285</td>\n",
       "      <td>529</td>\n",
       "      <td>23791</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1/1/2017</td>\n",
       "      <td>9/24/2003</td>\n",
       "      <td>SO61285</td>\n",
       "      <td>214</td>\n",
       "      <td>23791</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1/1/2017</td>\n",
       "      <td>9/4/2003</td>\n",
       "      <td>SO61285</td>\n",
       "      <td>540</td>\n",
       "      <td>23791</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1/1/2017</td>\n",
       "      <td>9/28/2003</td>\n",
       "      <td>SO61301</td>\n",
       "      <td>529</td>\n",
       "      <td>16747</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1/1/2017</td>\n",
       "      <td>10/21/2003</td>\n",
       "      <td>SO61301</td>\n",
       "      <td>377</td>\n",
       "      <td>16747</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  OrderDate   StockDate OrderNumber  ProductKey  CustomerKey  TerritoryKey  \\\n",
       "0  1/1/2017  12/13/2003     SO61285         529        23791             1   \n",
       "1  1/1/2017   9/24/2003     SO61285         214        23791             1   \n",
       "2  1/1/2017    9/4/2003     SO61285         540        23791             1   \n",
       "3  1/1/2017   9/28/2003     SO61301         529        16747             1   \n",
       "4  1/1/2017  10/21/2003     SO61301         377        16747             1   \n",
       "\n",
       "   OrderLineItem  OrderQuantity  \n",
       "0              2              2  \n",
       "1              3              1  \n",
       "2              1              1  \n",
       "3              2              2  \n",
       "4              1              1  "
      ]
     },
     "execution_count": 218,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "FS_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 219,
   "id": "45d0307e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ReturnIndex</th>\n",
       "      <th>ReturnDate</th>\n",
       "      <th>TerritoryKey</th>\n",
       "      <th>ProductKey</th>\n",
       "      <th>ReturnQuantity</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>1/18/2015</td>\n",
       "      <td>9</td>\n",
       "      <td>312</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>1/18/2015</td>\n",
       "      <td>10</td>\n",
       "      <td>310</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1/21/2015</td>\n",
       "      <td>8</td>\n",
       "      <td>346</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>1/22/2015</td>\n",
       "      <td>4</td>\n",
       "      <td>311</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>2/2/2015</td>\n",
       "      <td>6</td>\n",
       "      <td>312</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   ReturnIndex ReturnDate TerritoryKey ProductKey ReturnQuantity\n",
       "0            1  1/18/2015            9        312              1\n",
       "1            2  1/18/2015           10        310              1\n",
       "2            3  1/21/2015            8        346              1\n",
       "3            4  1/22/2015            4        311              1\n",
       "4            5   2/2/2015            6        312              1"
      ]
     },
     "execution_count": 219,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "FR_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 220,
   "id": "77fafb2c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "OrderDate        0\n",
       "StockDate        0\n",
       "OrderNumber      0\n",
       "ProductKey       0\n",
       "CustomerKey      0\n",
       "TerritoryKey     0\n",
       "OrderLineItem    0\n",
       "OrderQuantity    0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 220,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "## checking for isnull values in the dataframe\n",
    "\n",
    "FS_df.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "id": "a72ad30b",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 29481 entries, 0 to 29480\n",
      "Data columns (total 8 columns):\n",
      " #   Column         Non-Null Count  Dtype \n",
      "---  ------         --------------  ----- \n",
      " 0   OrderDate      29481 non-null  object\n",
      " 1   StockDate      29481 non-null  object\n",
      " 2   OrderNumber    29481 non-null  object\n",
      " 3   ProductKey     29481 non-null  int64 \n",
      " 4   CustomerKey    29481 non-null  int64 \n",
      " 5   TerritoryKey   29481 non-null  int64 \n",
      " 6   OrderLineItem  29481 non-null  int64 \n",
      " 7   OrderQuantity  29481 non-null  int64 \n",
      "dtypes: int64(5), object(3)\n",
      "memory usage: 1.8+ MB\n"
     ]
    }
   ],
   "source": [
    "FS_df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "id": "f0d99f96",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 18148 entries, 0 to 18147\n",
      "Data columns (total 13 columns):\n",
      " #   Column          Non-Null Count  Dtype \n",
      "---  ------          --------------  ----- \n",
      " 0   CustomerKey     18148 non-null  int64 \n",
      " 1   Prefix          18018 non-null  object\n",
      " 2   FirstName       18148 non-null  object\n",
      " 3   LastName        18148 non-null  object\n",
      " 4   BirthDate       18148 non-null  object\n",
      " 5   MaritalStatus   18148 non-null  object\n",
      " 6   Gender          18148 non-null  object\n",
      " 7   EmailAddress    18148 non-null  object\n",
      " 8   AnnualIncome    18148 non-null  object\n",
      " 9   TotalChildren   18148 non-null  int64 \n",
      " 10  EducationLevel  18148 non-null  object\n",
      " 11  Occupation      18148 non-null  object\n",
      " 12  HomeOwner       18148 non-null  object\n",
      "dtypes: int64(2), object(11)\n",
      "memory usage: 1.8+ MB\n"
     ]
    }
   ],
   "source": [
    "DCU_df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54322271",
   "metadata": {},
   "source": [
    "## Ensuring that the columns have the appropriate data types"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 223,
   "id": "0ee3f523",
   "metadata": {},
   "outputs": [],
   "source": [
    "### converting the string columns to a datetime data type\n",
    "\n",
    "FS_df['OrderDate'] = pd.to_datetime(FS_df['OrderDate'], errors='coerce')\n",
    "FS_df['StockDate'] = pd.to_datetime(FS_df['StockDate'], errors='coerce')\n",
    "DCAL_df['OrderDate'] = pd.to_datetime(DCAL_df['OrderDate'], errors='coerce')\n",
    "\n",
    "## Ensuring that numerical columns are properly typed\n",
    "\n",
    "FS_df['OrderQuantity'] = pd.to_numeric(FS_df['OrderQuantity'], errors='coerce').astype(int)\n",
    "FR_df['ReturnQuantity'] = pd.to_numeric(FR_df['ReturnQuantity'], errors='coerce').astype(int)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 224,
   "id": "eb7cdeab",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 29481 entries, 0 to 29480\n",
      "Data columns (total 8 columns):\n",
      " #   Column         Non-Null Count  Dtype         \n",
      "---  ------         --------------  -----         \n",
      " 0   OrderDate      29481 non-null  datetime64[ns]\n",
      " 1   StockDate      29481 non-null  datetime64[ns]\n",
      " 2   OrderNumber    29481 non-null  object        \n",
      " 3   ProductKey     29481 non-null  int64         \n",
      " 4   CustomerKey    29481 non-null  int64         \n",
      " 5   TerritoryKey   29481 non-null  int64         \n",
      " 6   OrderLineItem  29481 non-null  int64         \n",
      " 7   OrderQuantity  29481 non-null  int32         \n",
      "dtypes: datetime64[ns](2), int32(1), int64(4), object(1)\n",
      "memory usage: 1.7+ MB\n"
     ]
    }
   ],
   "source": [
    "## Confirming that the datatype has changed\n",
    "\n",
    "FS_df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 225,
   "id": "06573d1a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 1809 entries, 0 to 1808\n",
      "Data columns (total 5 columns):\n",
      " #   Column          Non-Null Count  Dtype \n",
      "---  ------          --------------  ----- \n",
      " 0   ReturnIndex     1809 non-null   int64 \n",
      " 1   ReturnDate      1809 non-null   object\n",
      " 2   TerritoryKey    1809 non-null   object\n",
      " 3   ProductKey      1809 non-null   object\n",
      " 4   ReturnQuantity  1809 non-null   int32 \n",
      "dtypes: int32(1), int64(1), object(3)\n",
      "memory usage: 63.7+ KB\n"
     ]
    }
   ],
   "source": [
    "FR_df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c01c6f6c",
   "metadata": {},
   "source": [
    "## Referential Integrity"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 226,
   "id": "38242075",
   "metadata": {},
   "outputs": [],
   "source": [
    "## check for valid productkey in the products table which connects to the factsales table\n",
    "\n",
    "invalid_product_keys = FS_df[~FS_df['ProductKey']. isin(DP_df['ProductKey'])]\n",
    "if not invalid_product_keys.empty:\n",
    "    print(\"invalid product key references found in FS_df \")\n",
    "\n",
    "## check for valid customerkey references in customers\n",
    "\n",
    "invalid_customer_keys = FS_df[~FS_df['CustomerKey']. isin(DCU_df['CustomerKey'])]\n",
    "if not invalid_customer_keys.empty:\n",
    "    print(\"invalid customer key references found in FS_df \")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 227,
   "id": "3de139a7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 18148 entries, 0 to 18147\n",
      "Data columns (total 13 columns):\n",
      " #   Column          Non-Null Count  Dtype \n",
      "---  ------          --------------  ----- \n",
      " 0   CustomerKey     18148 non-null  int64 \n",
      " 1   Prefix          18018 non-null  object\n",
      " 2   FirstName       18148 non-null  object\n",
      " 3   LastName        18148 non-null  object\n",
      " 4   BirthDate       18148 non-null  object\n",
      " 5   MaritalStatus   18148 non-null  object\n",
      " 6   Gender          18148 non-null  object\n",
      " 7   EmailAddress    18148 non-null  object\n",
      " 8   AnnualIncome    18148 non-null  object\n",
      " 9   TotalChildren   18148 non-null  int64 \n",
      " 10  EducationLevel  18148 non-null  object\n",
      " 11  Occupation      18148 non-null  object\n",
      " 12  HomeOwner       18148 non-null  object\n",
      "dtypes: int64(2), object(11)\n",
      "memory usage: 1.8+ MB\n"
     ]
    }
   ],
   "source": [
    "DCU_df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 228,
   "id": "03bb0e49",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>CustomerKey</th>\n",
       "      <th>Prefix</th>\n",
       "      <th>FirstName</th>\n",
       "      <th>LastName</th>\n",
       "      <th>BirthDate</th>\n",
       "      <th>MaritalStatus</th>\n",
       "      <th>Gender</th>\n",
       "      <th>EmailAddress</th>\n",
       "      <th>AnnualIncome</th>\n",
       "      <th>TotalChildren</th>\n",
       "      <th>EducationLevel</th>\n",
       "      <th>Occupation</th>\n",
       "      <th>HomeOwner</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>11000</td>\n",
       "      <td>MR.</td>\n",
       "      <td>JON</td>\n",
       "      <td>YANG</td>\n",
       "      <td>4/8/1966</td>\n",
       "      <td>M</td>\n",
       "      <td>M</td>\n",
       "      <td>jon24@adventure-works.com</td>\n",
       "      <td>$90,000</td>\n",
       "      <td>2</td>\n",
       "      <td>Bachelors</td>\n",
       "      <td>Professional</td>\n",
       "      <td>Y</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>11001</td>\n",
       "      <td>MR.</td>\n",
       "      <td>EUGENE</td>\n",
       "      <td>HUANG</td>\n",
       "      <td>5/14/1965</td>\n",
       "      <td>S</td>\n",
       "      <td>M</td>\n",
       "      <td>eugene10@adventure-works.com</td>\n",
       "      <td>$60,000</td>\n",
       "      <td>3</td>\n",
       "      <td>Bachelors</td>\n",
       "      <td>Professional</td>\n",
       "      <td>N</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>11002</td>\n",
       "      <td>MR.</td>\n",
       "      <td>RUBEN</td>\n",
       "      <td>TORRES</td>\n",
       "      <td>8/12/1965</td>\n",
       "      <td>M</td>\n",
       "      <td>M</td>\n",
       "      <td>ruben35@adventure-works.com</td>\n",
       "      <td>$60,000</td>\n",
       "      <td>3</td>\n",
       "      <td>Bachelors</td>\n",
       "      <td>Professional</td>\n",
       "      <td>Y</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>11003</td>\n",
       "      <td>MS.</td>\n",
       "      <td>CHRISTY</td>\n",
       "      <td>ZHU</td>\n",
       "      <td>2/15/1968</td>\n",
       "      <td>S</td>\n",
       "      <td>F</td>\n",
       "      <td>christy12@adventure-works.com</td>\n",
       "      <td>$70,000</td>\n",
       "      <td>0</td>\n",
       "      <td>Bachelors</td>\n",
       "      <td>Professional</td>\n",
       "      <td>N</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>11004</td>\n",
       "      <td>MRS.</td>\n",
       "      <td>ELIZABETH</td>\n",
       "      <td>JOHNSON</td>\n",
       "      <td>8/8/1968</td>\n",
       "      <td>S</td>\n",
       "      <td>F</td>\n",
       "      <td>elizabeth5@adventure-works.com</td>\n",
       "      <td>$80,000</td>\n",
       "      <td>5</td>\n",
       "      <td>Bachelors</td>\n",
       "      <td>Professional</td>\n",
       "      <td>Y</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   CustomerKey Prefix  FirstName LastName  BirthDate MaritalStatus Gender  \\\n",
       "0        11000    MR.        JON     YANG   4/8/1966             M      M   \n",
       "1        11001    MR.     EUGENE    HUANG  5/14/1965             S      M   \n",
       "2        11002    MR.      RUBEN   TORRES  8/12/1965             M      M   \n",
       "3        11003    MS.    CHRISTY      ZHU  2/15/1968             S      F   \n",
       "4        11004   MRS.  ELIZABETH  JOHNSON   8/8/1968             S      F   \n",
       "\n",
       "                     EmailAddress AnnualIncome  TotalChildren EducationLevel  \\\n",
       "0       jon24@adventure-works.com     $90,000               2      Bachelors   \n",
       "1    eugene10@adventure-works.com     $60,000               3      Bachelors   \n",
       "2     ruben35@adventure-works.com     $60,000               3      Bachelors   \n",
       "3   christy12@adventure-works.com     $70,000               0      Bachelors   \n",
       "4  elizabeth5@adventure-works.com     $80,000               5      Bachelors   \n",
       "\n",
       "     Occupation HomeOwner  \n",
       "0  Professional         Y  \n",
       "1  Professional         N  \n",
       "2  Professional         Y  \n",
       "3  Professional         N  \n",
       "4  Professional         Y  "
      ]
     },
     "execution_count": 228,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "DCU_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 229,
   "id": "37b4472b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 293 entries, 0 to 292\n",
      "Data columns (total 11 columns):\n",
      " #   Column                 Non-Null Count  Dtype  \n",
      "---  ------                 --------------  -----  \n",
      " 0   ProductKey             293 non-null    int64  \n",
      " 1   ProductSubcategoryKey  293 non-null    int64  \n",
      " 2   ProductSKU             293 non-null    object \n",
      " 3   ProductName            293 non-null    object \n",
      " 4   ModelName              293 non-null    object \n",
      " 5   ProductDescription     293 non-null    object \n",
      " 6   ProductColor           293 non-null    object \n",
      " 7   ProductSize            293 non-null    object \n",
      " 8   ProductStyle           293 non-null    object \n",
      " 9   ProductCost            293 non-null    float64\n",
      " 10  ProductPrice           293 non-null    float64\n",
      "dtypes: float64(2), int64(2), object(7)\n",
      "memory usage: 25.3+ KB\n"
     ]
    }
   ],
   "source": [
    "DP_df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "acec2a26",
   "metadata": {},
   "source": [
    "## Visualizing Outliers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 230,
   "id": "c1c027ca",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "# Boxplot for productprice to visualize outliers\n",
    "plt.figure(figsize=(6,4))\n",
    "plt.boxplot(DP_df['ProductPrice'].dropna())\n",
    "plt.title('Box Plot of product price')\n",
    "plt.xlabel('Product price')\n",
    "plt.show()\n",
    "\n",
    "\n",
    "plt.figure(figsize=(6, 4))\n",
    "# Scatter plot with the index of the DataFrame as x-axis and ProductPrice as y-axis\n",
    "plt.scatter(DP_df.index, DP_df['ProductPrice'].dropna())\n",
    "plt.title('Scatter Plot of Product Price')\n",
    "plt.xlabel('Index')\n",
    "plt.ylabel('Product Price')\n",
    "plt.grid(True)  # Add grid lines for better readability\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "02ffc7ba",
   "metadata": {},
   "source": [
    "## Removing the outliers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 215,
   "id": "b08b10d7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Removed 16 outliers from ProductPrice.\n"
     ]
    }
   ],
   "source": [
    "def remove_outliers_iqr(df, column): #This function removes outliers from a specified column in a DataFrame using the Interquartile Range (IQR) method.\n",
    "    Q1 =df[column].quantile(0.25) #Calculate the first quartile (Q1), which is the 25th percentile of the data in the specified column.\n",
    "    Q3 =df[column].quantile(0.75) #Calculate the third quartile (Q3), which is the 75th percentile of the data in the specified column.\n",
    "    IQR =Q3-Q1 #Calculate the Interquartile Range (IQR). IQR is the range between Q1 and Q3, capturing the middle 50% of the data.\n",
    "    lower_bound =Q1 -1.5 * IQR #defines the upper and lower bounds, any number lower or higher than these lower and upper bound will be considered an outlier.\n",
    "    upper_bound =Q3 + 1.5 * IQR\n",
    "    \n",
    "    #filters off the outliers\n",
    "    filtered_df =df[(df[column]>= lower_bound) & (df[column] <= upper_bound)]\n",
    "    \n",
    "    print(f\"Removed {len(df) - len(filtered_df)} outliers from {column}.\")\n",
    "    return filtered_df\n",
    "\n",
    "# removing the outliers\n",
    "DP_df_clean = remove_outliers_iqr(DP_df, \"ProductPrice\")\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
