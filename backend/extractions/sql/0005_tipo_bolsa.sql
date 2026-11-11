/*
  Migración de tipo de bolsa para SQL Server.
  Ejecutar una sola vez sobre la base SIICOBS después de realizar un respaldo.
  La tabla existente es dbo.extractions_extraction; no se crea ninguna tabla.
*/
SET XACT_ABORT ON;
BEGIN TRANSACTION;

IF COL_LENGTH('dbo.extractions_extraction', 'type_bag') IS NULL
BEGIN
    ALTER TABLE dbo.extractions_extraction
        ADD type_bag varchar(24) NULL;
END;

/* Clasifica los códigos históricos antes de normalizar la cantidad. */
UPDATE dbo.extractions_extraction
SET type_bag = CASE bags_quantity
    WHEN 1 THEN 'SIMPLE'
    WHEN 2 THEN 'DOBLE'
    WHEN 3 THEN 'TRIPLE'
    WHEN 4 THEN 'CUADRUPLE'
    WHEN 5 THEN 'CUADRUPLE_CON_FILTRO'
    WHEN 6 THEN 'SET_AFERESIS'
    ELSE type_bag
END
WHERE type_bag IS NULL;

/* 5 y 6 eran códigos de tipo; ahora la cantidad real es 4 y 2. */
UPDATE dbo.extractions_extraction
SET bags_quantity = CASE bags_quantity
    WHEN 5 THEN 4
    WHEN 6 THEN 2
END
WHERE bags_quantity IN (5, 6);

IF EXISTS (
    SELECT 1
    FROM dbo.extractions_extraction
    WHERE type_bag IS NULL
       OR type_bag NOT IN (
           'SIMPLE', 'DOBLE', 'TRIPLE', 'CUADRUPLE',
           'CUADRUPLE_CON_FILTRO', 'SET_AFERESIS'
       )
       OR NOT (
           (type_bag = 'SIMPLE' AND bags_quantity = 1) OR
           (type_bag = 'DOBLE' AND bags_quantity = 2) OR
           (type_bag = 'TRIPLE' AND bags_quantity = 3) OR
           (type_bag = 'CUADRUPLE' AND bags_quantity = 4) OR
           (type_bag = 'CUADRUPLE_CON_FILTRO' AND bags_quantity = 4) OR
           (type_bag = 'SET_AFERESIS' AND bags_quantity = 2)
       )
)
BEGIN
    THROW 50001, 'Hay extracciones con tipo o cantidad de bolsa no reconocidos. Revise los datos antes de continuar.', 1;
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.default_constraints dc
    INNER JOIN sys.columns c
        ON c.object_id = dc.parent_object_id
       AND c.column_id = dc.parent_column_id
    WHERE dc.parent_object_id = OBJECT_ID('dbo.extractions_extraction')
      AND c.name = 'type_bag'
)
BEGIN
    ALTER TABLE dbo.extractions_extraction
        ADD CONSTRAINT DF_extractions_extraction_type_bag
        DEFAULT ('SIMPLE') FOR type_bag;
END;

ALTER TABLE dbo.extractions_extraction
    ALTER COLUMN type_bag varchar(24) NOT NULL;

IF NOT EXISTS (
    SELECT 1
    FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('dbo.extractions_extraction')
      AND name = 'extraction_type_bag_quantity_valid'
)
BEGIN
    ALTER TABLE dbo.extractions_extraction
        ADD CONSTRAINT extraction_type_bag_quantity_valid CHECK (
            (type_bag = 'SIMPLE' AND bags_quantity = 1) OR
            (type_bag = 'DOBLE' AND bags_quantity = 2) OR
            (type_bag = 'TRIPLE' AND bags_quantity = 3) OR
            (type_bag = 'CUADRUPLE' AND bags_quantity = 4) OR
            (type_bag = 'CUADRUPLE_CON_FILTRO' AND bags_quantity = 4) OR
            (type_bag = 'SET_AFERESIS' AND bags_quantity = 2)
        );
END;

COMMIT TRANSACTION;
