SELECT Id, Quantity, TotalAmount, Status FROM dbo.OrderDetail WHERE Status NOT IN ('Cancel') AND TotalAmount > 0

