/*
  Migración de bloqueo de liberación por anticuerpos irregulares positivos.
  Ejecutar una sola vez sobre SQL Server después de realizar un respaldo.
  Se agrega una columna a dbo.packages_typehemocomponent; no se crea otra tabla.
*/
SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;

    IF COL_LENGTH('dbo.packages_typehemocomponent', 'blocks_release_with_irregular_antibodies') IS NULL
    BEGIN
        ALTER TABLE dbo.packages_typehemocomponent
            ADD blocks_release_with_irregular_antibodies bit NULL;
    END;

    /* Marca los tres tipos que no se pueden liberar con resultado positivo. */
    UPDATE dbo.packages_typehemocomponent
    SET blocks_release_with_irregular_antibodies = 1
    WHERE UPPER(LTRIM(RTRIM(name))) IN (
        'PLASMA FRESCO CONGELADO',
        'CRIOPRECIPITADO',
        'CONCENTRADO DE PLAQUETAS'
    );

    /* Los demás tipos quedan permitidos por defecto. */
    UPDATE dbo.packages_typehemocomponent
    SET blocks_release_with_irregular_antibodies = 0
    WHERE blocks_release_with_irregular_antibodies IS NULL;

    ALTER TABLE dbo.packages_typehemocomponent
        ALTER COLUMN blocks_release_with_irregular_antibodies bit NOT NULL;

    IF NOT EXISTS (
        SELECT 1
        FROM sys.default_constraints dc
        INNER JOIN sys.columns c
            ON c.object_id = dc.parent_object_id
           AND c.column_id = dc.parent_column_id
        WHERE dc.parent_object_id = OBJECT_ID('dbo.packages_typehemocomponent')
          AND c.name = 'blocks_release_with_irregular_antibodies'
    )
    BEGIN
        ALTER TABLE dbo.packages_typehemocomponent
            ADD CONSTRAINT DF_packages_typehemocomponent_blocks_release_irregular_antibodies
            DEFAULT (0) FOR blocks_release_with_irregular_antibodies;
    END;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
