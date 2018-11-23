#student.db记录微信端绑定的学生信息，以及饭卡号与金额的对应
student.db{
	STUDENT{
		WeChatID            TEXT,
		StudentID           TEXT,
		StudentName         TEXT,
		ParentName          TEXT,
		ParentTel           TEXT,
		HomeAddress         TEXT,
		MealCard            TEXT,
		TIM	                TEXT
	}
	MEALCARD{
		MealCard            TEXT,
		MealCardMoney       TEXT
	}
}

#mealcard.db按照饭卡号记录消费记录，字段P为微信充值的回调原文
mealcard.db{
	100{...},
	101{
		TIM	                 TEXT,
		RECORD               TEXT,
		ReduceMealCardMoney  TEXT,
		Number               TEXT,
		MoneyNow             TEXT,
		ReduceMealCardId     TEXT,
		p                    TEXT
	}
}

#updatadb.db按照日期记录消费记录
updatadb.db{
	2018-09-01{...},
	2018-09-02{
		TIM                     TEXT,
		RECORD                  TEXT,
		ReduceMealCardMoney     TEXT,
		Number                  TEXT,
		MoneyNow                TEXT,
		ReduceMealCardId        TEXT,
		types                   TEXT,
		MoneyOld                TEXT
}
}








